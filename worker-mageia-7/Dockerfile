FROM mageia:7

RUN urpmi.addmedia --distrib http://www.mirrorservice.org/sites/mageia.org/pub/mageia/distrib/7/x86_64
RUN urpmi.update -a
RUN urpmi --auto-update
RUN urpmi --force lib64mesaegl1
RUN urpmi --force notification-daemon
RUN urpmi --force urpmi-debuginfo-install python lib64python2.7-stdlib
RUN urpmi --force git tar rpmdevtools make cmake glibc gcc-c++ man gettext
RUN urpmi --force desktop-file-utils appstream-util libappstream-glib8 hicolor-icon-theme
RUN urpmi --force dbus-devel
RUN urpmi --force libgnutls-devel
RUN urpmi --force lib64boost-devel
RUN urpmi --force lib64protobuf-devel
RUN urpmi --force protobuf-compiler
RUN urpmi --force lib64sqlite3-devel
RUN urpmi --force lib64alsa2-devel
RUN urpmi --force lib64pulseaudio-devel
RUN urpmi --force lib64notify-devel
RUN urpmi --force lib64qt5core-devel lib64qt5gui-devel lib64qt5widgets-devel lib64qt5network-devel lib64qt5concurrent-devel \
                  lib64qt5sql-devel lib64qt5dbus-devel lib64qt5x11extras-devel lib64qt5help-devel libqt5test-devel qt5ct
RUN urpmi --force lib64gstreamer1.0-devel lib64gstreamer-plugins-base1.0-devel
RUN urpmi --force lib64cdio-devel lib64gpod-devel lib64plist-devel lib64usbmuxd-devel lib64mtp-devel
RUN urpmi --force lib64raw1394-devel
RUN urpmi --force lib64taglib-devel
RUN urpmi --force lib64chromaprint-devel
RUN urpmi --force libfftw-devel
RUN urpmi --force python3 libpython3-devel python3-pip

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==2.6.0

RUN echo "mageia-7" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}


CMD ["/usr/bin/python3", "/config/worker/start.py"]
