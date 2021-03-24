FROM opensuse/tumbleweed

RUN sed -i 's/baseurl=.*/baseurl=http:\/\/ftp.uninett.no\/pub\/linux\/opensuse\/tumbleweed\/repo\/oss\//g' /etc/zypp/repos.d/repo-oss.repo

RUN zypper -n ar -c -f -n 'repo-packman' https://ftp.gwdg.de/pub/linux/misc/packman/suse/openSUSE_Tumbleweed/ repo-packman
RUN zypper -n ar -c -f -n 'repo-libraries' https://download.opensuse.org/repositories/home:/jonaski:/libraries/openSUSE_Tumbleweed/ repo-libraries

RUN zypper -n --gpg-auto-import-keys ref
RUN zypper -n --gpg-auto-import-keys dup -l -y

RUN zypper -n --gpg-auto-import-keys install \
    git make cmake gcc gcc-c++ tar gettext-tools wget \
    lsb-release rpm-build squashfs patchelf desktop-file-utils \
    glibc-devel glib2-devel glib2-tools dbus-1-devel libgnutls-devel alsa-devel libpulse-devel libnotify-devel \
    boost-devel libboost_headers-devel protobuf-devel sqlite3-devel fftw3-devel taglib-devel \
    libQt5Core-devel libQt5Gui-devel libQt5Widgets-devel libQt5Concurrent-devel libQt5Network-devel libQt5Sql-devel libQt5DBus-devel libQt5Test-devel \
    libqt5-qtx11extras-devel libqt5-qtbase-common-devel libQt5Sql5-sqlite libqt5-qtwayland libqt5-qtdeclarative-tools libqt5-linguist-devel \
    gstreamer-devel gstreamer-plugins-base-devel \
    libcdio-devel libgpod-devel libplist-devel libmtp-devel libusbmuxd-devel libchromaprint-devel \
    desktop-file-utils update-desktop-files appstream-glib AppStream hicolor-icon-theme \
    python3-base python3-devel python3-pip go \
    gstreamer gstreamer-plugins-base gstreamer-plugins-good \
    gstreamer-plugins-bad gstreamer-plugins-bad-orig-addon gstreamer-plugins-ugly gstreamer-plugins-ugly-orig-addon \
    gstreamer-plugins-libav \
    alsa alsa-plugins-oss alsa-plugins-upmix alsa-plugins-pulse alsa-plugins-jack

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==3.0.2

RUN echo "appimage-qt5" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

RUN mkdir -p /home/buildbot/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown buildbot /home/buildbot/rpmbuild/{,BUILD,RPMS,SOURCES,SPECS,SRPMS}

RUN rm -rf /tmp/strawberry-appimagetool
RUN cd /tmp && git clone https://github.com/strawberrymusicplayer/strawberry-appimagetool
RUN cd /tmp/strawberry-appimagetool/appimagetool && go build -trimpath -ldflags="-s -w"
RUN cp /tmp/strawberry-appimagetool/appimagetool/appimagetool /usr/local/bin/
RUN rm -f /usr/local/bin/runtime-x86_64 && wget -P /usr/local/bin https://github.com/AppImage/AppImageKit/releases/download/continuous/runtime-x86_64

CMD ["/usr/bin/python3", "/config/worker/start.py"]
