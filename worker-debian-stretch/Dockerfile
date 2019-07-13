from debian:stretch

run apt-get -y update
run apt-get -y upgrade
run apt-get install -y \
                    git make cmake gcc fakeroot gettext \
                    python3-pip python3-dev \
                    libglib2.0-dev dpkg-dev libdbus-1-dev libboost-dev libprotobuf-dev protobuf-compiler libsqlite3-dev sqlite3 libgnutls28-dev \
                    libasound2-dev libpulse-dev \
                    qtbase5-dev qtbase5-dev-tools qtbase5-private-dev \
                    libqt5core5a libqt5gui5 libqt5widgets5 libqt5concurrent5 libqt5network5 libqt5sql5 \
                    libqt5x11extras5-dev libqt5dbus5 qttools5-dev \
                    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-alsa gstreamer1.0-pulseaudio \
                    libchromaprint-dev libfftw3-dev \
                    libcdio-dev libmtp-dev libgpod-dev libimobiledevice-dev libplist-dev libusbmuxd-dev

run pip3 install --upgrade pip
run pip3 install buildbot_worker==2.3.0

run echo "debian-stretch" > /worker-name
run useradd -r -m -s /bin/false buildbot

cmd ["/usr/bin/python3", "/config/worker/start.py"]
