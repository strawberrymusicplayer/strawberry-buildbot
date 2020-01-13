FROM opensuse/tumbleweed

RUN zypper -n ar -c -f -n 'repo-tools' https://download.opensuse.org/repositories/devel:/tools/openSUSE_Tumbleweed/ repo-tools
RUN zypper -n ar -c -f -n 'repo-mingw' https://download.opensuse.org/repositories/windows:/mingw:/win32/openSUSE_Tumbleweed/ repo-mingw

RUN zypper --non-interactive --gpg-auto-import-keys ref
RUN zypper --non-interactive --gpg-auto-import-keys dup -l -y
RUN zypper --non-interactive --gpg-auto-import-keys up -l -y

RUN zypper --non-interactive --gpg-auto-import-keys install \
    python-base python-devel python3-base python3-devel python3-pip python-xml \
    which wget patch tar gperf gzip bzip2 xz p7zip p7zip-full zip unzip lzip gettext-tools gtk-doc \
    git make cmake libtool gcc-c++ pkg-config autoconf automake intltool ruby scons bison flex \
    linux-glibc-devel glibc glibc-devel glibc-extra glibc-locale glibc-i18ndata glibc-32bit gdk-pixbuf-devel \
    mingw32-cross-nsis meson ninja file-devel libopenssl-devel

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==2.5.1

RUN echo "mingw" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

CMD ["/usr/bin/python3", "/config/worker/start.py"]
