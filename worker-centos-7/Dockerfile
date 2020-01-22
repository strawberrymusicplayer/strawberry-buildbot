FROM centos:7

RUN yum install --assumeyes epel-release wget

RUN cd /tmp && wget http://awel.domblogger.net/7/media/x86_64/awel-media-release-7-6.noarch.rpm && rpm -i awel-media-release-7-6.noarch.rpm

RUN yum clean all
RUN yum update --assumeyes
RUN yum install --assumeyes \
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

RUN yum install --assumeyes gstreamer1-devel gstreamer1-plugins-base-devel gstreamer1-plugins-bad-devel \
                            gstreamer1 gstreamer1-plugins-base gstreamer1-plugins-good gstreamer1-plugins-bad gstreamer1-plugins-ugly gstreamer1-libav \
                            gstreamer1-plugins-good-jack

RUN yum install --assumeyes python36-pip python36-devel

RUN yum clean all && yum update --assumeyes

RUN pip3.6 install --upgrade pip
RUN pip3.6 install buildbot_worker==2.6.0

RUN ln -s /usr/bin/cmake3 /usr/bin/cmake

RUN echo "centos-7" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

# SQLite3 with FTS5 support
# Compile newest version of sqlite3 because centos provides too old version without FTS5

RUN cd /tmp && wget https://www.sqlite.org/2020/sqlite-autoconf-3310000.tar.gz
RUN cd /tmp && tar -xvf sqlite-autoconf-3310000.tar.gz
RUN cd /tmp/sqlite-autoconf-3310000 && ./configure --prefix=/usr --libdir=/usr/lib64 --disable-static --disable-static-shell --enable-fts4 --enable-fts3 --enable-fts5
RUN cd /tmp/sqlite-autoconf-3310000 && make
RUN cd /tmp/sqlite-autoconf-3310000 && make install
RUN ldconfig

# TagLib
#RUN cd /tmp && git clone https://github.com/taglib/taglib
#RUN cd /tmp/taglib && git pull
#RUN cd /tmp/taglib/taglib/toolkit && sed -i 's/#define TAGLIB_PATCH_VERSION 1/#define TAGLIB_PATCH_VERSION 2/g' taglib.h
#RUN cd /tmp/taglib && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

# Chromaprint
RUN cd /tmp && wget https://github.com/acoustid/chromaprint/releases/download/v1.4.3/chromaprint-1.4.3.tar.gz && tar -xf chromaprint-1.4.3.tar.gz
RUN cd /tmp/chromaprint-v1.4.3 && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=ON -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

# AppImageKit
RUN cd /tmp && git clone https://github.com/AppImage/AppImageKit
RUN cd /tmp/AppImageKit && git submodule update --init --recursive
RUN mkdir -p /tmp/AppImageKit/build
RUN cd /tmp/AppImageKit/build && cmake ..
RUN cd /tmp/AppImageKit/build && make -j4
RUN cp /tmp/AppImageKit/build/src/appimagetool /usr/local/bin/
RUN mkdir -p /usr/local/lib/appimagekit/
RUN cp /tmp/AppImageKit/build/mksquashfs-prefix/mksquashfs /usr/local/lib/appimagekit/

# linuxdeploy
RUN cd /tmp && git clone https://github.com/linuxdeploy/linuxdeploy
RUN cd /tmp/linuxdeploy && git submodule update --init --recursive
RUN mkdir -p /tmp/linuxdeploy/build
RUN cd /tmp/linuxdeploy/build && cmake .. -DUSE_SYSTEM_CIMG=OFF
RUN cd /tmp/linuxdeploy/build && make -j4
RUN cp /tmp/linuxdeploy/build/bin/* /usr/local/bin/

# linuxdeploy-plugin-qt
RUN cd /tmp && git clone https://github.com/linuxdeploy/linuxdeploy-plugin-qt
RUN cd /tmp/linuxdeploy-plugin-qt && git submodule update --init --recursive
RUN mkdir -p /tmp/linuxdeploy-plugin-qt/build
RUN cd /tmp/linuxdeploy-plugin-qt/build && cmake .. -DUSE_SYSTEM_CIMG=OFF
RUN cd /tmp/linuxdeploy-plugin-qt/build && make -j4
RUN cp /tmp/linuxdeploy-plugin-qt/build/bin/* /usr/local/bin/

# linuxdeploy-plugin-appimage
RUN cd /tmp && git clone https://github.com/linuxdeploy/linuxdeploy-plugin-appimage
RUN cd /tmp/linuxdeploy-plugin-appimage && git submodule update --init --recursive
RUN mkdir -p /tmp/linuxdeploy-plugin-appimage/build
RUN cd /tmp/linuxdeploy-plugin-appimage/build && cmake ..
RUN cd /tmp/linuxdeploy-plugin-appimage/build && make -j4
RUN cp /tmp/linuxdeploy-plugin-appimage/build/src/linuxdeploy-plugin-appimage /usr/local/bin/


CMD ["/usr/bin/python3.6", "/config/worker/start.py"]
