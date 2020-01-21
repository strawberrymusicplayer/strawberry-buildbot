FROM debian:stretch

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y \
                    git make cmake gcc fakeroot gettext lsb-release \
                    python3-pip python3-dev \
                    libglib2.0-dev dpkg-dev libdbus-1-dev libboost-dev libprotobuf-dev protobuf-compiler libsqlite3-dev sqlite3 libgnutls28-dev \
                    libasound2-dev libpulse-dev \
                    qtbase5-dev qtbase5-dev-tools qtbase5-private-dev \
                    libqt5core5a libqt5gui5 libqt5widgets5 libqt5concurrent5 libqt5network5 libqt5sql5 \
                    libqt5x11extras5-dev libqt5dbus5 qttools5-dev \
                    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-alsa gstreamer1.0-pulseaudio \
                    libchromaprint-dev libfftw3-dev \
                    libcdio-dev libmtp-dev libgpod-dev libimobiledevice-dev libplist-dev libusbmuxd-dev

RUN pip3 install --upgrade pip
RUN pip3 install buildbot_worker==2.5.1

RUN echo "debian-stretch" > /worker-name
RUN useradd -r -m -s /bin/false buildbot

CMD ["/usr/bin/python3", "/config/worker/start.py"]
