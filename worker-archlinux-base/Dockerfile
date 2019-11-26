from archlinux/base

run pacman -Syu --noconfirm
run pacman -S --noconfirm \
                    git make cmake gcc fakeroot sudo pkgconf python-pip gettext \
                    desktop-file-utils hicolor-icon-theme \
                    udisks2 dbus sqlite3 alsa-lib pulseaudio boost protobuf gnutls \
                    qt5-base qt5-x11extras qt5-tools \
                    gst-plugins-base gst-plugins-good xine-lib vlc phonon-qt5 \
                    taglib chromaprint \
                    libcdio libmtp libgpod libusbmuxd libplist libimobiledevice

run pacman -S --noconfirm fftw

run pip3 install --upgrade pip
run pip3 install buildbot_worker==2.5.1

run echo "archlinux-base" > /worker-name
run echo "PACKAGER=\"Jonas Kvinge <jonas@strawbs.net>\"" >>/etc/makepkg.conf
run useradd -r -m -s /bin/false buildbot

cmd ["/usr/bin/python3", "/config/worker/start.py"]
