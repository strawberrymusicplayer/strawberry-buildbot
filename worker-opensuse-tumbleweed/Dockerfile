from opensuse/tumbleweed

run zypper --non-interactive --gpg-auto-import-keys ref
run zypper --non-interactive --gpg-auto-import-keys dup -l -y

run zypper --non-interactive --gpg-auto-import-keys install \
    lsb-release rpm-build rpmdevtools \
    git tar make cmake gcc gcc-c++ pkg-config gettext-tools \
    desktop-file-utils update-desktop-files appstream-glib AppStream hicolor-icon-theme \
    fuse libfuse2 \
    python3-base python3-devel python3-pip \
    glibc-devel glib2-devel glib2-tools dbus-1-devel alsa-devel libpulse-devel libnotify-devel libgnutls-devel \
    boost-devel libboost_headers-devel protobuf-devel sqlite3-devel taglib-devel fftw3-devel \
    gstreamer-devel gstreamer-plugins-base-devel libxine-devel vlc-devel \
    libQt5Core-devel libQt5Gui-devel libQt5Widgets-devel libQt5Concurrent-devel libQt5Network-devel libQt5Sql-devel libQt5DBus-devel \
    libqt5-qtx11extras-devel libqt5-qtbase-common-devel libQt5Sql5-sqlite libqt5-qtwayland libqt5-qtdeclarative-tools libqt5-linguist-devel \
    libcdio-devel libgpod-devel libplist-devel libmtp-devel libusbmuxd-devel libchromaprint-devel \
    gstreamer-plugins-base gstreamer-plugins-good gstreamer-plugins-bad gstreamer-plugins-ugly gstreamer-plugins-libav

run pip3 install --upgrade pip
run pip3 install buildbot_worker==2.3.1

run echo "opensuse-tumbleweed" > /worker-name
run useradd -r -m -s /bin/false buildbot

run mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}
cmd ["/usr/bin/python3", "/config/worker/start.py"]
