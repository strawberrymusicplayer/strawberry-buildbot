from centos:7

run yum install --assumeyes epel-release wget

run cd /tmp && wget http://awel.domblogger.net/7/media/x86_64/awel-media-release-7-6.noarch.rpm && rpm -i awel-media-release-7-6.noarch.rpm

run yum clean all
run yum update --assumeyes
run yum install --assumeyes \
    redhat-lsb-core \
    git tar rpmdevtools make cmake3 glib glibc gcc-c++ man gettext wget fuse fuse-libs fuse-devel \
    desktop-file-utils libappstream-glib appstream-data \
    dbus-devel boost-devel protobuf-devel protobuf-compiler alsa-lib-devel pulseaudio-libs-devel libnotify-devel gnutls-devel \
    qt5-devel qt5-qtbase-devel qt5-qtx11extras-devel qt5-qttools-devel \
    libcdio-devel libgpod-devel libplist-devel libusbmuxd-devel libmtp-devel fftw-devel \
    libchromaprint-devel \
    dbus-x11 xorg-x11-server-Xvfb xorg-x11-xauth \
    ffmpeg-devel fftw-devel \
    hicolor-icon-theme adwaita-qt5 \
    patchelf ccache libjpeg-devel automake libtool vim-common cairo-devel

run yum install --assumeyes gstreamer1-devel gstreamer1-plugins-base-devel gstreamer1-plugins-bad-devel \
                            gstreamer1 gstreamer1-plugins-base gstreamer1-plugins-good gstreamer1-plugins-bad gstreamer1-plugins-ugly gstreamer1-libav \
                            gstreamer1-plugins-good-jack

run yum install --assumeyes python36-pip python36-devel

run yum clean all && yum update --assumeyes

run pip3.6 install --upgrade pip
run pip3.6 install buildbot_worker==2.4.0

run ln -s /usr/bin/cmake3 /usr/bin/cmake

run echo "centos-7" > /worker-name
run useradd -r -m -s /bin/false buildbot

run mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

# SQLite3 with FTS5 support
# Compile newest version of sqlite3 because centos provides too old version without FTS5

run cd /tmp && wget https://www.sqlite.org/2019/sqlite-autoconf-3290000.tar.gz
run cd /tmp && tar -xvf sqlite-autoconf-3290000.tar.gz
run cd /tmp/sqlite-autoconf-3290000 && ./configure --prefix=/usr --libdir=/usr/lib64 --disable-static --disable-static-shell --enable-fts4 --enable-fts3 --enable-fts5
run cd /tmp/sqlite-autoconf-3290000 && make
run cd /tmp/sqlite-autoconf-3290000 && make install
run ldconfig

# TagLib
#run cd /tmp && git clone https://github.com/taglib/taglib
#run cd /tmp/taglib && git pull
#run cd /tmp/taglib/taglib/toolkit && sed -i 's/#define TAGLIB_PATCH_VERSION 1/#define TAGLIB_PATCH_VERSION 2/g' taglib.h
#run cd /tmp/taglib && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

# Chromaprint
run cd /tmp && wget https://github.com/acoustid/chromaprint/releases/download/v1.4.3/chromaprint-1.4.3.tar.gz && tar -xf chromaprint-1.4.3.tar.gz
run cd /tmp/chromaprint-v1.4.3 && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=ON -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

# AppImageKit
run cd /tmp && git clone https://github.com/AppImage/AppImageKit
run cd /tmp/AppImageKit && git submodule update --init --recursive
run mkdir -p /tmp/AppImageKit/build
run cd /tmp/AppImageKit/build && cmake ..
run cd /tmp/AppImageKit/build && make -j4
run cp /tmp/AppImageKit/build/src/appimagetool /usr/local/bin/
run mkdir -p /usr/local/lib/appimagekit/
run cp /tmp/AppImageKit/build/mksquashfs-prefix/mksquashfs /usr/local/lib/appimagekit/

# linuxdeploy
run cd /tmp && git clone https://github.com/linuxdeploy/linuxdeploy
run cd /tmp/linuxdeploy && git submodule update --init --recursive
run mkdir -p /tmp/linuxdeploy/build
run cd /tmp/linuxdeploy/build && cmake .. -DUSE_SYSTEM_CIMG=OFF
run cd /tmp/linuxdeploy/build && make -j4
run cp /tmp/linuxdeploy/build/bin/* /usr/local/bin/

# linuxdeploy-plugin-qt
run cd /tmp && git clone https://github.com/linuxdeploy/linuxdeploy-plugin-qt
run cd /tmp/linuxdeploy-plugin-qt && git submodule update --init --recursive
run mkdir -p /tmp/linuxdeploy-plugin-qt/build
run cd /tmp/linuxdeploy-plugin-qt/build && cmake .. -DUSE_SYSTEM_CIMG=OFF
run cd /tmp/linuxdeploy-plugin-qt/build && make -j4
run cp /tmp/linuxdeploy-plugin-qt/build/bin/* /usr/local/bin/

# linuxdeploy-plugin-appimage
run cd /tmp && git clone https://github.com/linuxdeploy/linuxdeploy-plugin-appimage
run cd /tmp/linuxdeploy-plugin-appimage && git submodule update --init --recursive
run mkdir -p /tmp/linuxdeploy-plugin-appimage/build
run cd /tmp/linuxdeploy-plugin-appimage/build && cmake ..
run cd /tmp/linuxdeploy-plugin-appimage/build && make -j4
run cp /tmp/linuxdeploy-plugin-appimage/build/src/linuxdeploy-plugin-appimage /usr/local/bin/


cmd ["/usr/bin/python3.6", "/config/worker/start.py"]
