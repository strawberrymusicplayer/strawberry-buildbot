from centos:7

run yum install --assumeyes epel-release wget

run cd /tmp && wget http://awel.domblogger.net/7/media/x86_64/awel-media-release-7-6.noarch.rpm && rpm -i awel-media-release-7-6.noarch.rpm

run yum clean all
run yum update --assumeyes
run yum install --assumeyes \
    redhat-lsb-core \
    git tar rpmdevtools make cmake glib glibc gcc-c++ man gettext wget fuse fuse-libs \
    desktop-file-utils libappstream-glib appstream-data \
    dbus-devel boost-devel protobuf-devel protobuf-compiler sqlite-devel alsa-lib-devel pulseaudio-libs-devel libnotify-devel \
    qt5-devel qt5-qtbase-devel qt5-qtx11extras-devel qt5-qttools-devel \
    libcdio-devel libgpod-devel libplist-devel libusbmuxd-devel libmtp-devel \
    taglib-devel libchromaprint-devel \
    dbus-x11 xorg-x11-server-Xvfb xorg-x11-xauth \
    ffmpeg-devel fftw-devel \
    hicolor-icon-theme adwaita-qt5

run yum install --assumeyes gstreamer1-devel gstreamer1-plugins-base-devel gstreamer1-plugins-bad-devel \
                            gstreamer1 gstreamer1-plugins-base gstreamer1-plugins-good gstreamer1-plugins-bad gstreamer1-plugins-ugly gstreamer1-libav \
                            gstreamer1-plugins-good-jack

run yum install --assumeyes python36-pip python36-devel

run yum clean all && yum update --assumeyes

run pip3.6 install --upgrade pip
run pip3.6 install buildbot_worker==2.1.0

run echo "centos-7" > /worker-name
run useradd -r -m -s /bin/false buildbot

run mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

run cd /tmp && wget https://github.com/acoustid/chromaprint/releases/download/v1.4.3/chromaprint-1.4.3.tar.gz
run cd /tmp && tar -xf chromaprint-1.4.3.tar.gz
run cd /tmp && cd chromaprint-v1.4.3 && \
  cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=ON -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

cmd ["/usr/bin/python3.6", "/config/worker/start.py"]
