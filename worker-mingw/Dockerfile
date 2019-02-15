from opensuse/leap

run zypper -n ar -c -f -n 'repo-tools' https://download.opensuse.org/repositories/devel:/tools/openSUSE_Leap_15.0/ repo-tools
#run zypper -n ar -c -f -n 'repo-devel-languages-haskell' https://download.opensuse.org/repositories/devel:/languages:/haskell/openSUSE_Tumbleweed/ repo-devel-languages-haskell

run zypper --non-interactive --gpg-auto-import-keys ref
run zypper --non-interactive --gpg-auto-import-keys dup -l -y
run zypper --non-interactive --gpg-auto-import-keys up -l -y

run zypper --non-interactive --gpg-auto-import-keys install \
    python-base python-devel python3-base python3-devel python3-pip \
    which wget patch tar gperf unzip p7zip gettext-tools gtk-doc \
    git make cmake libtool gcc-c++ pkg-config autoconf automake intltool ruby scons bison flex  \
    gdk-pixbuf-devel \
    linux-glibc-devel glibc glibc-devel glibc-extra glibc-locale glibc-i18ndata glibc-32bit \
    ghc-nsis

# p7zip-full

run pip3 install buildbot_worker==1.6.0

run echo "mingw" > /worker-name
run useradd -r -m -s /bin/false buildbot

cmd ["/usr/bin/python3", "/config/worker/start.py"]
