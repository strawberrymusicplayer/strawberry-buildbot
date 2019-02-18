# Strawberry Buildbot

import os.path
import pprint

from buildbot.changes import gitpoller
from buildbot.plugins import steps, util
from buildbot.process import factory
from buildbot.steps import master
from buildbot.steps import shell
from buildbot.steps import transfer
from buildbot.steps.source import git

UPLOADBASE = "/srv/www/htdocs/builds"
UPLOADURL = "http://builds.strawbs.org"


def GitBaseUrl(repository):
  return "https://github.com/jonaski/%s.git" % repository


def GitArgs(repository, branch):
  return {
    "repourl": GitBaseUrl(repository),
    "branch": branch,
    "mode": "incremental",
    "retry": (5 * 60, 3),
    "workdir": "source",
  }


def GitPoller(repository, branch):
  return gitpoller.GitPoller(
      project=repository.lower(),
      repourl=GitBaseUrl(repository),
      pollinterval=60 * 5,  # seconds
      branch=branch,
      workdir="gitpoller_%s_%s" % (repository.lower(), branch))

@util.renderer

def get_base_filename(props):

  output_filepath = props.getProperty('output-filepath')
  base_filename = os.path.basename(output_filepath)

  return {
    "output-filepath": output_filepath,
    "base-filename": base_filename,
  }


def UploadPackage(directory):

  return transfer.FileUpload(
    #mode=0644,
    workdir="source",
    workersrc=util.Interpolate("%(prop:output-filepath)s"),
    masterdest=util.Interpolate(
      "%(kw:base)s/%(kw:directory)s/%(prop:base-filename)s",
      base=UPLOADBASE,
      directory=directory,
    ),
    url=util.Interpolate(
      "%(kw:base)s/%(kw:directory)s/%(prop:base-filename)s",
      base=UPLOADURL,
      directory=directory,
    ),
  )


def MakeSourceBuilder():

  git_args = GitArgs("strawberry", "master")
  git_args["mode"] = "full"
  git_args["method"] = "fresh"

  cmake_cmd = [
    "cmake",
    "..",
  ]

  f = factory.BuildFactory()
  f.addStep(git.Git(**git_args))

  f.addStep(
    shell.ShellCommand(
      name="rm -rf build",
      workdir="source",
      haltOnFailure=True,
      command=["rm", "-rf", "build"]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="cmake",
      command=cmake_cmd,
      haltOnFailure=True,
      workdir="source/build"
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="rm -f *.bz2",
      workdir="source/dist/scripts",
      haltOnFailure=True,
      command=["rm", "-f", "*.bz2"]
    )
  )
    
  f.addStep(
    shell.ShellCommand(
      command=["./maketarball.sh"],
      haltOnFailure=True,
      workdir="source/dist/scripts")
  )

  f.addStep(steps.SetPropertyFromCommand(
    name="get output filename",
    command=[
      "sh", "-c",
      "ls -dt " + "dist/scripts/strawberry-*.tar.xz" + " | head -n 1"
    ],
    workdir="source",
    property="output-filepath",
  ))
  f.addStep(steps.SetProperties(properties=get_base_filename))
  f.addStep(UploadPackage("source"))
  return f


def MakeRPMBuilder(distro, version):

  f = factory.BuildFactory()
  f.addStep(git.Git(**GitArgs("strawberry", "master")))

  f.addStep(
    shell.ShellCommand(
      name="clean rmpbuild",
      workdir="source/build",
      command="find ~/rpmbuild/ -type f -delete"
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="rm -rf build",
      workdir="source",
      haltOnFailure=True,
      command=["rm", "-rf", "build"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="cmake",
      workdir="source/build",
      haltOnFailure=True,
      command=["cmake", "../"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="make clean",
      workdir="source/build",
      haltOnFailure=True,
      command=["make", "clean"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="maketarball",
      workdir="source/build",
      haltOnFailure=True,
      command=["../dist/scripts/maketarball.sh"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="movetarball",
      workdir="source/build",
      haltOnFailure=True,
      command="mv strawberry-*.tar.xz ~/rpmbuild/SOURCES")
  )
  f.addStep(
    shell.Compile(
      name="rpmbuild",
      workdir="source/build",
      haltOnFailure=True,
      command=["rpmbuild", "-ba", "../dist/" + distro + "/strawberry.spec"]
    )
  )

  f.addStep(steps.SetPropertyFromCommand(
    name="get output filename",
    command=[
      "sh", "-c",
      "ls -dt " + "~/rpmbuild/RPMS/*/strawberry-*.rpm" + " | grep -v debuginfo | grep -v debugsource | head -n 1"
    ],
    workdir="source",
    property="output-filepath",
  ))
  f.addStep(steps.SetProperties(properties=get_base_filename))
  f.addStep(UploadPackage(distro + "/" + version))
  return f


def MakeDebBuilder(distro, version):

  env = {"DEB_BUILD_OPTIONS": "parallel=4",}

  cmake_cmd = [
    "cmake",
    "..",
    "-DWITH_DEBIAN=ON",
    "-DDEB_ARCH=amd64",
    "-DDEB_DIST=" + version,
    #"-DFORCE_GIT_REVISION=",
  ]

  f = factory.BuildFactory()
  f.addStep(git.Git(**GitArgs("strawberry", "master")))

  f.addStep(
    shell.ShellCommand(
      name="rm -rf build",
      workdir="source",
      haltOnFailure=True,
      command=["rm", "-rf", "build"]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="cmake",
      command=cmake_cmd,
      haltOnFailure=True,
      workdir="source/build"))

  f.addStep(
    shell.ShellCommand(
      name="make clean",
      workdir="source/build",
      haltOnFailure=True,
      command=["make", "clean"]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="copy deb",
      workdir="source/build",
      haltOnFailure=True,
      command="cp -v -r ../dist/debian ."))

  f.addStep(
    shell.Compile(
      name="dpkg-buildpackage",
      command=[
        "dpkg-buildpackage", "-b", "-d", "-uc", "-us",
      ],
      haltOnFailure=True,
      workdir="source/build"))

  f.addStep(steps.SetPropertyFromCommand(
    name="get output filename",
    command=[
      "sh", "-c",
      "ls -dt " + "strawberry_*.deb" + " | grep -v debuginfo | head -n 1"
    ],
    workdir="source",
    property="output-filepath",
  ))
  f.addStep(steps.SetProperties(properties=get_base_filename))

  f.addStep(UploadPackage("%s/%s" % (distro, version)))
  return f


def MakePacmanBuilder(distro, version):

  f = factory.BuildFactory()
  f.addStep(git.Git(**GitArgs("strawberry", "master")))

  f.addStep(
    shell.ShellCommand(
      name="rm -rf build",
      workdir="source",
      haltOnFailure=True,
      command=["rm", "-rf", "build"]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="cmake",
      workdir="source/build",
      haltOnFailure=True,
      command=["cmake", "../"]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="make clean",
      workdir="source/build",
      haltOnFailure=True,
      command=["make", "clean"]
    )
  )

  f.addStep(
    shell.Compile(
      name="makepkg",
      command=[
        "makepkg", "-f"
      ],
      haltOnFailure=True,
      workdir="source/dist/pacman"
    )
  )

  f.addStep(steps.SetPropertyFromCommand(
    name="get output filename",
    command=[
      "sh", "-c",
      "ls -dt " + "dist/pacman/strawberry-*.pkg.tar.xz" + " | head -n 1"
    ],
    workdir="source",
    property="output-filepath",
  ))
  f.addStep(steps.SetProperties(properties=get_base_filename))

  f.addStep(UploadPackage(distro))

  return f


def MakeAppImageBuilder(name):

  f = factory.BuildFactory()
  f.addStep(git.Git(**GitArgs("strawberry", "master")))

  #f.addStep(
  #  shell.ShellCommand(
  #    name="rm -rf build",
  #    workdir="source",
  #    haltOnFailure=True,
  #    command=["rm", "-rf", "build"]
  #  )
  #)

  f.addStep(
    shell.ShellCommand(
      name="cmake",
      workdir="source/build",
      haltOnFailure=True,
      command=["cmake", "..", "-DCMAKE_INSTALL_PREFIX=/usr"]
    )
  )

  f.addStep(steps.SetPropertyFromCommand(
    name="git describe --tags --always",
    command=["git", "describe", "--tags", "--always"],
    workdir="source",
    property="output-version",
  ))
  env_output = {
    "OUTPUT": util.Interpolate("Strawberry%(kw:name)s-%(prop:output-version)s.AppImage", name=name)
  }

  f.addStep(
    shell.Compile(
      name="make",
      workdir="source/build",
      haltOnFailure=True,
      command=["make", "-j", "8"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="make install",
      workdir="source/build",
      haltOnFailure=True,
      command=["make", "install", "DESTDIR=AppDir"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="Remove screenshot from appdata file",
      workdir="source/build",
      command=["sed", "-i", '/.*caption.*/d', "./AppDir/usr/share/metainfo/strawberry.appdata.xml"],
      haltOnFailure=True,
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="Remove screenshot from appdata file",
      workdir="source/build",
      command=["sed", "-i", '/.*screenshot.*/d', "./AppDir/usr/share/metainfo/strawberry.appdata.xml"],
      haltOnFailure=True,
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="Change appdata filename",
      workdir="source/build",
      haltOnFailure=True,
      command=["mv", "./AppDir/usr/share/metainfo/strawberry.appdata.xml", "./AppDir/usr/share/metainfo/org.strawbs.strawberry.appdata.xml"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="Change desktop filename",
      workdir="source/build",
      haltOnFailure=True,
      command=["mv", "./AppDir/usr/share/applications/strawberry.desktop", "./AppDir/usr/share/applications/org.strawbs.strawberry.desktop"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="curl linuxdeploy-x86_64.AppImage",
      workdir="source/build",
      haltOnFailure=True,
      command=["curl", "-O", "-L", "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="curl linuxdeploy-plugin-appimage-x86_64.AppImage",
      workdir="source/build",
      haltOnFailure=True,
      command=["curl", "-O", "-L", "https://github.com/linuxdeploy/linuxdeploy-plugin-appimage/releases/download/continuous/linuxdeploy-plugin-appimage-x86_64.AppImage"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="curl linuxdeploy-plugin-qt-x86_64.AppImage",
      workdir="source/build",
      haltOnFailure=True,
      command=["curl", "-O", "-L", "https://github.com/linuxdeploy/linuxdeploy-plugin-qt/releases/download/continuous/linuxdeploy-plugin-qt-x86_64.AppImage"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="chmod",
      workdir="source/build",
      haltOnFailure=True,
      command="chmod +x linuxdeploy*.AppImage"
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="linuxdeploy --appimage-extract",
      workdir="source/build",
      haltOnFailure=True,
      command=["./linuxdeploy-x86_64.AppImage", "--appimage-extract"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="linuxdeploy-plugin-appimage --appimage-extract",
      workdir="source/build",
      haltOnFailure=True,
      command=["./linuxdeploy-plugin-appimage-x86_64.AppImage", "--appimage-extract"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="linuxdeploy-plugin-qt-x86_64.AppImage --appimage-extract",
      workdir="source/build",
      haltOnFailure=True,
      command=["./linuxdeploy-plugin-qt-x86_64.AppImage", "--appimage-extract"]
    )
  )
  f.addStep(
    shell.ShellCommand(
      name="linuxdeploy",
      workdir="source/build",
      env=env_output,
      haltOnFailure=True,
      command=["./squashfs-root/usr/bin/linuxdeploy", "--appdir", "AppDir", "-e", "strawberry", "--plugin", "qt", "--output", "appimage"]
    )
  )

  f.addStep(steps.SetPropertyFromCommand(
    name="get output filename",
    command=[
      "sh", "-c",
      "ls -dt " + "build/Strawberry*.AppImage" + " | head -n 1"
    ],
    workdir="source",
    property="output-filepath",
    haltOnFailure=True,
  ))
  f.addStep(steps.SetProperties(properties=get_base_filename))
  f.addStep(UploadPackage("appimage"))
  return f


def MakeMXEBuilder():

  f = factory.BuildFactory()
  f.addStep(git.Git(**GitArgs("strawberry-mxe", "master")))

  #f.addStep(
  #  shell.ShellCommand(
  #    name="clean", workdir="source", command=["make", "clean"]))

  f.addStep(
    shell.Compile(
      name="compile",
      workdir="source",
      command=["make", "-j8"],
      timeout=108000,
      haltOnFailure=True,
    )
  )

  f.addStep(
      shell.ShellCommand(
          name="remove strawberry*.exe (686-w64-mingw32.shared)",
          workdir="source/usr/i686-w64-mingw32.shared/apps/strawberry/bin",
          command="rm -f strawberry*.exe StrawberrySetup*.exe"))

  f.addStep(
      shell.ShellCommand(
          name="remove strawberry*.exe (x86_64-w64-mingw32.shared)",
          workdir="source/usr/x86_64-w64-mingw32.shared/apps/strawberry/bin",
          command="rm -f strawberry*.exe StrawberrySetup*.exe"))

  return f


def MakeWindowsBuilder(is_debug, is_64):

  env_lang = {
    "RC_LANG": "en_US.UTF-8",
    "RC_LC_ALL": "en_US.UTF-8",
    "RC_LC_CTYPE": "en_US.UTF-8",
    "RC_LC_TIME": "nb_NO.UTF-8",
    "RC_LC_NUMERIC": "nb_NO.UTF-8",
    "RC_LC_MONETARY": "nb_NO.UTF-8",
    "RC_LC_PAPER": "nb_NO.UTF-8",
  }

  mingw32_name = ("x86_64-w64-mingw32.shared" if is_64 else "i686-w64-mingw32.shared")

  env = {
    "PKG_CONFIG_LIBDIR": "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/pkgconfig",
    "PATH": ":".join([
      "/persistent-data/mingw/mxe/source/usr/x86_64-pc-linux-gnu/bin",
      "/usr/local/bin",
      "/usr/bin",
      "/bin",
    ]),
  }

  cmake_cmd = [
    "cmake",
    "..",
    "-DCMAKE_TOOLCHAIN_FILE=/config/dist/" + ("Toolchain-x86_64-w64-mingw32.cmake" if is_64 else "Toolchain-i686-w64-mingw32.cmake"),
    "-DCMAKE_BUILD_TYPE=" + ("Debug" if is_debug else "Release"),
    "-DENABLE_WIN32_CONSOLE=" + ("ON" if is_debug else "OFF"),
    "-DENABLE_DBUS=OFF",
    "-DENABLE_LIBGPOD=OFF",
    "-DENABLE_IMOBILEDEVICE=OFF",
    "-DENABLE_LIBMTP=OFF",
    "-DENABLE_XINE=" + ("ON" if is_debug else "OFF"),
    "-DENABLE_DEEZER=ON",
  ]

  executable_files = [
    "strawberry.exe",
    "strawberry-tagreader.exe",
  ]

  strip_command = "/persistent-data/mingw/mxe/source/usr/bin/" + mingw32_name + "-strip"
  nsi_filename = ("strawberry-debug-x64.nsi" if is_debug and is_64 else ("strawberry-debug-x86.nsi" if is_debug else ("strawberry-x64.nsi" if is_64 else "strawberry-x86.nsi")))

  nsi_files = [
    "strawberry-x86.nsi",
    "strawberry-x64.nsi",
    "strawberry-debug-x86.nsi",
    "strawberry-debug-x64.nsi",
    "Capabilities.nsh",
    "FileAssociation.nsh",
    "strawberry.ico",
  ]
  imageformats_files = [
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/qt5/plugins/imageformats/qgif.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/qt5/plugins/imageformats/qjpeg.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/qt5/plugins/imageformats/qico.dll",
  ]
  gstreamer_plugins_files = [
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstapetag.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstapp.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstasf.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstaiff.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstaudioconvert.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstaudiofx.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstaudioparsers.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstaudioresample.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstaudiotestsrc.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstautodetect.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstcoreelements.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstdirectsound.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstequalizer.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstfaad.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstflac.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstgio.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgsticydemux.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstid3demux.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstisomp4.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstlame.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstogg.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstopusparse.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstplayback.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstreplaygain.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstspectrum.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstspeex.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgsttaglib.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgsttypefindfunctions.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstvolume.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstvorbis.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstwavpack.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstwavparse.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstcdio.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgsttcp.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstudp.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstsoup.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/bin/gstreamer-1.0/libgstlibav.dll",
  ]

  xine_plugins_files=[
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_ao_out_directx2.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_ao_out_directx.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_decode_dts.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_decode_dvaudio.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_decode_faad.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_decode_gsm610.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_decode_lpcm.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_decode_mad.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_decode_mpc.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_decode_mpeg2.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_dmx_asf.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_dmx_audio.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_dmx_playlist.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_dmx_slave.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_flac.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_wavpack.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_xiph.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/xineplug_inp_cdda.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/post/xineplug_post_audio_filters.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/post/xineplug_post_goom.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/post/xineplug_post_mosaico.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/post/xineplug_post_planar.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/post/xineplug_post_switch.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/post/xineplug_post_tvtime.dll",
    "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/lib/xine/plugins/2.7/post/xineplug_post_visualizations.dll",
  ]

  f = factory.BuildFactory()
  f.addStep(git.Git(**GitArgs("strawberry", "master")))

  #f.addStep(
  #  shell.ShellCommand(
  #    name="rm -rf build",
  #    workdir="source",
  #    haltOnFailure=True,
  #    command=["rm", "-rf", "build"],
  #  )
  #)
  f.addStep(
    shell.ShellCommand(
      name="cmake",
      workdir="source/build",
      env=env,
      haltOnFailure=True,
      command=cmake_cmd,
    )
  )
  f.addStep(
    shell.Compile(
      command=["make", "-j8"], workdir="source/build", haltOnFailure=True)
  )
  f.addStep(
    shell.ShellCommand(
      name="strip",
      workdir="source/build",
      haltOnFailure=True,
      #env=env,
      command=[strip_command] + executable_files
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="mkdir platforms/sqldrivers/imageformats/gstreamer-plugins/xine-plugins",
      workdir="source/build",
      haltOnFailure=True,
      command=[
        "mkdir",
        "-p",
        "platforms",
        "sqldrivers",
        "imageformats",
        "gstreamer-plugins",
        "xine-plugins",
      ]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="copy qwindows.dll",
      workdir="source/build/platforms",
      haltOnFailure=True,
      command=[
        "cp",
        "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/qt5/plugins/platforms/qwindows.dll",
        ".",
      ]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="copy qsqlite.dll",
      workdir="source/build/sqldrivers",
      haltOnFailure=True,
      command=[
        "cp",
        "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/qt5/plugins/sqldrivers/qsqlite.dll",
        ".",
      ]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="copy imageformats",
      workdir="source/build/imageformats",
      haltOnFailure=True,
      command=[
        "cp",
        imageformats_files,
        ".",
      ]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="copy gstreamer-plugins",
      workdir="source/build/gstreamer-plugins",
      haltOnFailure=True,
      command=[
        "cp",
        gstreamer_plugins_files,
        ".",
      ]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="copy xine-plugins",
      workdir="source/build/xine-plugins",
      haltOnFailure=True,
      command=[
        "cp",
        xine_plugins_files,
        ".",
      ]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="copydlldeps.sh",
      workdir="source/build",
      haltOnFailure=True,
      command=[
        "/persistent-data/mingw/mxe/source/tools/copydlldeps.sh",
        "-c",
        "-d",
        ".",
        "-F",
        ".",
        "-F",
        "./platforms",
        "-F",
        "./sqldrivers",
        "-F",
        "./imageformats",
        "-F",
        "s./gstreamer-plugins",
        "-F",
        "./xine-plugins",
        "-X",
        "/persistent-data/mingw/mxe/source/usr/" + mingw32_name + "/apps",
        "-R",
        "/persistent-data/mingw/mxe/source/usr/" + mingw32_name,
      ]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="copy nsi files",
      workdir="source/dist/windows",
      haltOnFailure=True,
      command=[
        "cp",
        nsi_files,
        "../../build/",
      ]
    )
  )

  f.addStep(
    shell.ShellCommand(
      name="makensis",
      env=env_lang,
      command=["makensis", nsi_filename],
      workdir="source/build",
      haltOnFailure=True,
    )
  )

  f.addStep(steps.SetPropertyFromCommand(
    name="get output filename",
    command=[
      "sh",
      "-c",
      "ls -dt " + "build/StrawberrySetup-*.exe" + " | head -n 1"
    ],
    workdir="source",
    property="output-filepath",
  ))
  f.addStep(steps.SetProperties(properties=get_base_filename))

  f.addStep(UploadPackage("windows"))

  return f
