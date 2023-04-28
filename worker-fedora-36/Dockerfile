FROM fedora:36

RUN dnf update --assumeyes
RUN dnf upgrade --assumeyes
RUN dnf install --assumeyes \
    redhat-lsb-core \
    glibc gcc-c++ which git tar rpmdevtools make cmake glib man gettext \
    boost-devel dbus-devel protobuf-devel protobuf-compiler sqlite-devel alsa-lib-devel pulseaudio-libs-devel libnotify-devel gnutls-devel \
    qt6-qtbase-devel qt6-qtbase-private-devel qt6-qttools-devel \
    gstreamer1-devel gstreamer1-plugins-base-devel \
    libcdio-devel libgpod-devel libplist-devel libusbmuxd-devel libmtp-devel \
    taglib-devel libchromaprint-devel fftw-devel libicu-devel \
    dbus-x11 xorg-x11-server-Xvfb xorg-x11-xauth \
    desktop-file-utils libappstream-glib hicolor-icon-theme \
    python3 python3-devel python3-pip

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==3.8.0

RUN echo "fedora-36" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

RUN rm -rf /usr/lib64/cmake/Qt6Sql/{Qt6QMYSQL*,Qt6QODBCD*,Qt6QPSQL*}

CMD ["/usr/bin/python3", "/config/worker/start.py"]
