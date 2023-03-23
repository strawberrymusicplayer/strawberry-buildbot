FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive
RUN apt -y update
RUN apt -y upgrade
RUN apt install -y git make cmake gcc g++ fakeroot gettext lsb-release dput build-essential dh-make \
                   libboost-dev libglib2.0-dev dpkg-dev libdbus-1-dev libprotobuf-dev protobuf-compiler libsqlite3-dev libgnutls28-dev \
                   libasound2-dev libpulse-dev \
                   qtbase5-dev qtbase5-private-dev qtbase5-dev-tools qttools5-dev libqt5x11extras5-dev \
                   libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-alsa gstreamer1.0-pulseaudio \
                   libtag1-dev libchromaprint-dev libfftw3-dev libicu-dev \
                   libcdio-dev libmtp-dev libgpod-dev libimobiledevice-dev libplist-dev libusbmuxd-dev \
                   buildbot-worker

RUN echo "debian-bullseye" > /worker-name

CMD ["/usr/bin/python3", "/config/worker/start.py"]
