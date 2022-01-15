FROM openmandriva/cooker

RUN dnf update --assumeyes
RUN dnf upgrade --assumeyes
RUN dnf install --assumeyes \
    glibc gcc-c++ git gnutar make cmake glib gettext lsb-release rpmdevtools rpm-build \
    glibc-devel boost-devel dbus-devel protobuf-devel protobuf-compiler sqlite-devel libasound-devel pulseaudio-devel gnutls-devel lib64GL-devel \
    libgst-plugins-base1.0-devel taglib-devel chromaprint-devel fftw-devel libcdio-devel libgpod-devel libmtp-devel \
    lib64Qt6Core-devel lib64Qt6Concurrent-devel lib64Qt6Network-devel lib64Qt6Sql-devel lib64Qt6DBus-devel lib64Qt6Gui-devel lib64Qt6Widgets-devel lib64Qt6Test-devel qt6-cmake qt6-qtbase-tools qt6-qttools \
    desktop-file-utils appstream appstream-util hicolor-icon-theme \
    python3 python3-devel python3-pip

RUN cp /usr/bin/gtar /bin/tar

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==3.4.0

RUN echo "openmandriva-cooker" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
RUN chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

CMD ["/usr/bin/python3", "/config/worker/start.py"]
