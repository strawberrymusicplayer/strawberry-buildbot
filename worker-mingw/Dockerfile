from opensuse/tumbleweed

run zypper -n ar -c -f -n 'repo-tools' https://download.opensuse.org/repositories/devel:/tools/openSUSE_Tumbleweed/ repo-tools
run zypper -n ar -c -f -n 'repo-mingw' https://download.opensuse.org/repositories/windows:/mingw:/win32/openSUSE_Tumbleweed/ repo-mingw

run zypper --non-interactive --gpg-auto-import-keys ref
run zypper --non-interactive --gpg-auto-import-keys dup -l -y
run zypper --non-interactive --gpg-auto-import-keys up -l -y

run zypper --non-interactive --gpg-auto-import-keys install \
    python-base python-devel python3-base python3-devel python3-pip python-xml \
    which wget patch tar gperf gzip bzip2 xz p7zip p7zip-full unzip lzip gettext-tools gtk-doc \
    git make cmake libtool gcc-c++ pkg-config autoconf automake intltool ruby scons bison flex \
    linux-glibc-devel glibc glibc-devel glibc-extra glibc-locale glibc-i18ndata glibc-32bit gdk-pixbuf-devel \
    mingw32-cross-nsis meson ninja

run pip3 install --upgrade pip
run pip3 install buildbot_worker==2.4.0

run echo "mingw" > /worker-name
run useradd -r -m -s /bin/false buildbot

cmd ["/usr/bin/python3", "/config/worker/start.py"]
