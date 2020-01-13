FROM centos:8

RUN dnf install -y epel-release
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
RUN dnf install -y 'dnf-command(config-manager)'
RUN dnf config-manager --set-enabled PowerTools

RUN dnf clean all
RUN dnf update -y
RUN dnf install -y \
                   redhat-lsb-core git tar wget man gettext fuse fuse-libs fuse-devel \
                   rpmdevtools make automake libtool cmake3 glibc gcc-c++ patchelf ccache \
                   desktop-file-utils libappstream-glib appstream-data \
                   dbus-devel boost-devel libnotify-devel gnutls-devel \
                   protobuf-devel protobuf-compiler \
                   alsa-lib-devel pulseaudio-libs-devel \
                   qt5-devel qt5-qtbase-devel qt5-qtx11extras-devel qt5-qttools-devel \
                   libcdio-devel libgpod-devel libplist-devel libusbmuxd-devel libmtp-devel \
                   fftw-devel libchromaprint-devel \
                   dbus-x11 xorg-x11-server-Xvfb xorg-x11-xauth hicolor-icon-theme \
                   libjpeg-devel vim-common cairo-devel \
                   python3-pip python3-devel

RUN dnf install -y gstreamer1-devel gstreamer1-plugins-base-devel \
                   gstreamer1 gstreamer1-plugins-base gstreamer1-plugins-good
                   #gstreamer1-plugins-bad gstreamer1-plugins-ugly gstreamer1-libav gstreamer1-plugins-bad-devel
                   #gstreamer1-plugins-good-jack


RUN dnf clean all && dnf update -y

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==2.5.1

RUN echo "centos-8" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

# SQLite3 with FTS5 support
# Compile newest version of sqlite3 because centos provides too old version without FTS5

RUN cd /tmp && wget https://www.sqlite.org/2019/sqlite-autoconf-3300100.tar.gz
RUN cd /tmp && tar -xvf sqlite-autoconf-3300100.tar.gz
RUN cd /tmp/sqlite-autoconf-3300100 && ./configure --prefix=/usr --libdir=/usr/lib64 --disable-static --disable-static-shell --enable-fts4 --enable-fts3 --enable-fts5
RUN cd /tmp/sqlite-autoconf-3300100 && make
RUN cd /tmp/sqlite-autoconf-3300100 && make install
RUN ldconfig

# TagLib
#RUN cd /tmp && git clone https://github.com/taglib/taglib
#RUN cd /tmp/taglib && git pull
#RUN cd /tmp/taglib/taglib/toolkit && sed -i 's/#define TAGLIB_PATCH_VERSION 1/#define TAGLIB_PATCH_VERSION 2/g' taglib.h
#RUN cd /tmp/taglib && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

# Chromaprint
#RUN cd /tmp && wget https://github.com/acoustid/chromaprint/releases/download/v1.4.3/chromaprint-1.4.3.tar.gz && tar -xf chromaprint-1.4.3.tar.gz
#RUN cd /tmp/chromaprint-v1.4.3 && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=ON -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

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


CMD ["/usr/bin/python3", "/config/worker/start.py"]
