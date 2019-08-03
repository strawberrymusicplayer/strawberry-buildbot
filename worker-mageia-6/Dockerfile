from mageia:6

run urpmi.addmedia --distrib http://www.mirrorservice.org/sites/mageia.org/pub/mageia/distrib/6/x86_64
run urpmi.update -a
run urpmi --auto-update
run urpmi --force lib64mesaegl1
run urpmi --force notification-daemon
run urpmi --force git tar rpmdevtools make cmake glibc gcc-c++ man gettext
run urpmi --force desktop-file-utils appstream-util libappstream-glib8 hicolor-icon-theme
run urpmi --force dbus-devel
run urpmi --force libgnutls-devel
run urpmi --force lib64boost-devel
run urpmi --force lib64protobuf-devel
run urpmi --force protobuf-compiler
run urpmi --force lib64sqlite3-devel
run urpmi --force lib64alsa2-devel
run urpmi --force lib64pulseaudio-devel
run urpmi --force lib64notify-devel
run urpmi --force lib64qt5core-devel lib64qt5gui-devel lib64qt5widgets-devel lib64qt5network-devel lib64qt5concurrent-devel \
                  lib64qt5sql-devel lib64qt5dbus-devel lib64qt5x11extras-devel lib64qt5help-devel libqt5test-devel qt5ct
run urpmi --force lib64gstreamer1.0-devel lib64gstreamer-plugins-base1.0-devel
run urpmi --force lib64cdio-devel lib64gpod-devel lib64plist-devel lib64usbmuxd-devel lib64mtp-devel
run urpmi --force lib64raw1394-devel
#run urpmi --force lib64taglib-devel
run urpmi --force lib64chromaprint-devel
run urpmi --force libfftw-devel
run urpmi --force python3 libpython3-devel
run urpmi --force gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-pulse

run pip3 install --upgrade pip
run pip3 install buildbot_worker==2.3.1

run echo "mageia-6" > /worker-name
run useradd -r -m -s /bin/false buildbot

run mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

# TagLib
#run cd /tmp && git clone https://github.com/taglib/taglib
#run cd /tmp/taglib && git pull
#run cd /tmp/taglib/taglib/toolkit && sed -i 's/#define TAGLIB_PATCH_VERSION 1/#define TAGLIB_PATCH_VERSION 2/g' taglib.h
#run cd /tmp/taglib && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DLIB_SUFFIX=64 . && make install

cmd ["/usr/bin/python3", "/config/worker/start.py"]
