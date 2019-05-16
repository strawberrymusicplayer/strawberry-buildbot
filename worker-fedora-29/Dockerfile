from fedora:29

run yum update --assumeyes
run dnf install --assumeyes \
    redhat-lsb-core python3 python3-devel \
    git tar rpmdevtools make cmake glib glibc gcc-c++ man gettext \
    desktop-file-utils libappstream-glib hicolor-icon-theme \
    dbus-devel boost-devel protobuf-devel protobuf-compiler sqlite-devel alsa-lib-devel pulseaudio-libs-devel libnotify-devel gnutls-devel \
    qt5-devel qt5-qtbase-devel qt5-qtx11extras-devel qt5-qttools-devel \
    gstreamer1-devel gstreamer1-plugins-base-devel \
    libcdio-devel libgpod-devel libplist-devel libusbmuxd-devel libmtp-devel \
    taglib-devel libchromaprint-devel fftw-devel \
    dbus-x11 xorg-x11-server-Xvfb xorg-x11-xauth

run pip3 install --upgrade pip
run pip3 install buildbot_worker==2.3.0

run echo "fedora-29" > /worker-name
run useradd -r -m -s /bin/false buildbot

run mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

cmd ["/usr/bin/python3", "/config/worker/start.py"]
