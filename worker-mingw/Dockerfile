from opensuse:tumbleweed

run zypper -n ar -c -f -n 'repo-tools' https://download.opensuse.org/repositories/devel:/tools/openSUSE_Tumbleweed/ repo-tools

run zypper --non-interactive --gpg-auto-import-keys ref
run zypper --non-interactive --gpg-auto-import-keys dup -l -y
run zypper --non-interactive --gpg-auto-import-keys up -l -y

run zypper --non-interactive --gpg-auto-import-keys install \
    python-base python-devel python2-pip \
    which wget patch tar gperf unzip p7zip p7zip-full gettext-tools gtk-doc \
    git make cmake libtool gcc-c++ pkg-config autoconf automake intltool ruby scons bison flex  \
    gdk-pixbuf-devel \
    linux-glibc-devel glibc glibc-devel glibc-extra glibc-locale glibc-locale-32bit glibc-i18ndata glibc-32bit \
    nsis

run pip install buildbot_worker==1.6.0

run echo "mingw" > /worker-name
run useradd -r -m -s /bin/false buildbot

cmd ["/usr/bin/python2", "/config/worker/start.py"]
