FROM opensuse/leap:15.3

RUN zypper -n ar -c -f -n 'repo-devel-tools-building' https://download.opensuse.org/repositories/devel:/tools:/building/openSUSE_Leap_15.3/ repo-devel-tools-building
RUN zypper -n ar -c -f -n 'repo-mingw' https://download.opensuse.org/repositories/windows:/mingw:/win32/openSUSE_Leap_15.3/ repo-mingw

RUN zypper -n --gpg-auto-import-keys ref
RUN zypper -n --gpg-auto-import-keys up -l -y

RUN zypper -n --gpg-auto-import-keys install \
    glibc glibc-extra glibc-locale glibc-i18ndata glibc-32bit gcc-c++ \
    shadow which patch gperf wget curl git ruby diffutils \
    make cmake libtool pkg-config autoconf automake meson ninja intltool makeinfo scons bison flex gettext-tools \
    tar gzip bzip2 xz p7zip p7zip-full lzip zip unzip orc \
    linux-glibc-devel glibc-devel file-devel libopenssl-devel gdk-pixbuf-devel gtk-doc \
    mingw32-cross-nsis \
    python-base python-devel python3-base python3-devel python3-pip python-xml python3-Mako

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==3.3.0

RUN mkdir -p /tmp/lockedlist && wget https://nsis.sourceforge.io/mediawiki/images/d/d3/LockedList.zip --directory-prefix=/tmp/lockedlist
RUN cd /tmp/lockedlist && unzip /tmp/lockedlist/LockedList.zip
RUN cp /tmp/lockedlist/Plugins/x86-unicode/LockedList.dll /usr/share/nsis/Plugins/x86-unicode/
RUN cp /tmp/lockedlist/Plugins/LockedList64.dll /usr/share/nsis/Plugins/

RUN echo "mingw" > /worker-name

RUN useradd -r -m -s /bin/false buildbot

CMD ["/usr/bin/python3", "/config/worker/start.py"]
