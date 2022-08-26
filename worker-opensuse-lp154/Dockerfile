FROM opensuse/leap:15.4

RUN zypper -n --gpg-auto-import-keys ref
RUN zypper -n --gpg-auto-import-keys up -l -y

RUN zypper -n --gpg-auto-import-keys install \
    lsb-release rpm-build rpmdevtools \
    git make cmake gcc11 gcc11-c++ tar gettext-tools \
    glibc-devel glib2-devel glib2-tools dbus-1-devel alsa-devel libpulse-devel libnotify-devel libgnutls-devel \
    boost-devel protobuf-devel sqlite3-devel taglib-devel libicu-devel \
    qt6-core-devel qt6-gui-devel qt6-gui-private-devel qt6-widgets-devel qt6-concurrent-devel qt6-network-devel \
    qt6-sql-devel qt6-dbus-devel qt6-test-devel qt6-base-common-devel qt6-sql-sqlite qt6-linguist-devel \
    gstreamer-devel gstreamer-plugins-base-devel vlc-devel \
    libcdio-devel libgpod-devel libplist-devel libmtp-devel libusbmuxd-devel libchromaprint-devel \
    desktop-file-utils update-desktop-files appstream-glib hicolor-icon-theme \
    python3-base python3-devel python3-pip

RUN update-alternatives --install /usr/bin/cc cc /usr/bin/gcc-11 50
RUN update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++-11 50
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 50
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 50
RUN update-alternatives --set cc /usr/bin/gcc-11
RUN update-alternatives --set c++ /usr/bin/g++-11
RUN update-alternatives --set gcc /usr/bin/gcc-11
RUN update-alternatives --set g++ /usr/bin/g++-11

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==3.6.0

RUN echo "opensuse-lp154" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}
CMD ["/usr/bin/python3", "/config/worker/start.py"]
