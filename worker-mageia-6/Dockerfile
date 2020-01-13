FROM mageia:6

RUN urpmi.addmedia --distrib http://www.mirrorservice.org/sites/mageia.org/pub/mageia/distrib/6/x86_64
RUN urpmi.update -a
RUN urpmi --auto-update
RUN urpmi --force lib64mesaegl1
RUN urpmi --force notification-daemon
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
#RUN urpmi --force lib64taglib-devel
RUN urpmi --force lib64chromaprint-devel
RUN urpmi --force libfftw-devel
RUN urpmi --force python3 libpython3-devel
RUN urpmi --force gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-pulse

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==2.5.1

RUN echo "mageia-6" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

# TagLib
#RUN cd /tmp && git clone https://github.com/taglib/taglib
#RUN cd /tmp/taglib && git pull
#RUN cd /tmp/taglib/taglib/toolkit && sed -i 's/#define TAGLIB_PATCH_VERSION 1/#define TAGLIB_PATCH_VERSION 2/g' taglib.h
#RUN cd /tmp/taglib && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

CMD ["/usr/bin/python3", "/config/worker/start.py"]
