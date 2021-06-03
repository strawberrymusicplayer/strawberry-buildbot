FROM opensuse/tumbleweed

RUN sed -i 's/baseurl=.*/baseurl=http:\/\/ftp.uninett.no\/pub\/linux\/opensuse\/tumbleweed\/repo\/oss\//g' /etc/zypp/repos.d/repo-oss.repo

RUN zypper -n --gpg-auto-import-keys ref
RUN zypper -n --gpg-auto-import-keys dup -l -y

RUN zypper -n --gpg-auto-import-keys install \
    lsb-release rpm-build \
    git make cmake gcc gcc-c++ tar gettext-tools \
    glibc-devel glib2-devel glib2-tools dbus-1-devel libgnutls-devel alsa-devel libpulse-devel libnotify-devel \
    boost-devel libboost_headers-devel protobuf-devel sqlite3-devel fftw3-devel taglib-devel \
    qt6-core-devel qt6-gui-devel qt6-gui-private-devel qt6-widgets-devel qt6-concurrent-devel qt6-network-devel \
    qt6-sql-devel qt6-dbus-devel qt6-test-devel qt6-base-common-devel qt6-sql-sqlite qt6-linguist-devel \
    gstreamer-devel gstreamer-plugins-base-devel vlc-devel \
    libcdio-devel libgpod-devel libplist-devel libmtp-devel libusbmuxd-devel libchromaprint-devel \
    desktop-file-utils update-desktop-files appstream-glib AppStream hicolor-icon-theme \
    python3-base python3-devel python3-pip

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==3.1.1

RUN echo "opensuse-tumbleweed" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}
CMD ["/usr/bin/python3", "/config/worker/start.py"]
