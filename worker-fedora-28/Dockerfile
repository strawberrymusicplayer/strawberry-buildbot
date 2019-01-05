from fedora:28

run dnf install --assumeyes \
    redhat-lsb-core python2 python2-devel \
    git tar rpmdevtools make cmake glib glibc gcc-c++ man \
    desktop-file-utils libappstream-glib hicolor-icon-theme \
    dbus-devel boost-devel protobuf-devel protobuf-compiler sqlite-devel alsa-lib-devel pulseaudio-libs-devel libnotify-devel \
    qt5-devel qt5-qtbase-devel qt5-qtx11extras-devel qt5-qttools-devel \
    gstreamer1-devel gstreamer1-plugins-base-devel \
    libcdio-devel libgpod-devel libplist-devel libusbmuxd-devel libmtp-devel \
    taglib-devel libchromaprint-devel \
    dbus-x11 xorg-x11-server-Xvfb xorg-x11-xauth

run pip install --upgrade pip
run pip install buildbot_worker==1.6.0

run echo "fedora-28" > /worker-name
run useradd -r -m -s /bin/false buildbot

run mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

cmd ["/usr/bin/python", "/config/worker/start.py"]
