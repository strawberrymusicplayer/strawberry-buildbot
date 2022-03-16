FROM opensuse/leap:15.3

RUN zypper -n ar -c -f -n 'repo-devel-tools-building' https://download.opensuse.org/repositories/devel:/tools:/building/openSUSE_Leap_15.3/ repo-devel-tools-building
RUN zypper -n ar -c -f -n 'repo-mingw' https://download.opensuse.org/repositories/windows:/mingw:/win32/openSUSE_Leap_15.3/ repo-mingw

RUN zypper -n --gpg-auto-import-keys ref
RUN zypper -n --gpg-auto-import-keys up -l -y

RUN zypper -n --gpg-auto-import-keys install \
    glibc glibc-extra glibc-locale glibc-i18ndata glibc-32bit gcc10 gcc10-c++ cpp10 \
    shadow which patch gperf wget curl git diffutils \
    make cmake libtool pkg-config autoconf automake makeinfo meson ninja intltool \
    tar gzip bzip2 xz p7zip p7zip-full lzip zip unzip \
    gtk-doc gettext-tools scons bison flex ruby orc \
    linux-glibc-devel glibc-devel file-devel libopenssl-devel libffi-devel gdk-pixbuf-devel libzstd-devel \
    python3-base python3-devel python3-pip python3-Mako \
    mingw32-cross-nsis

RUN update-alternatives --install /usr/bin/cc cc /usr/bin/gcc-10 50
RUN update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++-10 50
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 50
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 50
RUN update-alternatives --set cc /usr/bin/gcc-10
RUN update-alternatives --set c++ /usr/bin/g++-10
RUN update-alternatives --set gcc /usr/bin/gcc-10
RUN update-alternatives --set g++ /usr/bin/g++-10

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==3.4.0

RUN mkdir -p /tmp/lockedlist && wget https://nsis.sourceforge.io/mediawiki/images/d/d3/LockedList.zip --directory-prefix=/tmp/lockedlist
RUN cd /tmp/lockedlist && unzip /tmp/lockedlist/LockedList.zip
RUN cp /tmp/lockedlist/Plugins/x86-unicode/LockedList.dll /usr/share/nsis/Plugins/x86-unicode/
RUN cp /tmp/lockedlist/Plugins/LockedList64.dll /usr/share/nsis/Plugins/

RUN mkdir -p /tmp/registry && wget https://nsis.sourceforge.io/mediawiki/images/4/47/Registry.zip --directory-prefix=/tmp/registry
RUN cd /tmp/registry && unzip /tmp/registry/Registry.zip
RUN cp /tmp/registry/Desktop/Plugin/registry.dll /usr/share/nsis/Plugins/
RUN cp /tmp/registry/Desktop/Plugin/registry.dll /usr/share/nsis/Plugins/x86-unicode/

RUN mkdir -p /tmp/inetc && wget https://nsis.sourceforge.io/mediawiki/images/c/c9/Inetc.zip --directory-prefix=/tmp/inetc
RUN cd /tmp/inetc && unzip /tmp/inetc/Inetc.zip
RUN cp /tmp/inetc/Plugins/x86-unicode/INetC.dll /usr/share/nsis/Plugins/x86-unicode/

RUN echo "mingw" > /worker-name

RUN useradd -r -m -s /bin/false buildbot

CMD ["/usr/bin/python3", "/config/worker/start.py"]
