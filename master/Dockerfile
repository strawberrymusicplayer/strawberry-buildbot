FROM opensuse/leap:15.2

RUN zypper --non-interactive --gpg-auto-import-keys ref
RUN zypper --non-interactive --gpg-auto-import-keys up -l -y
RUN zypper --non-interactive --gpg-auto-import-keys install git gcc python3-pip python3-devel libcairo2 cairo-tools python3-cairo

RUN pip3 install --upgrade pip
RUN pip3 install pycairo requests buildbot==2.8.2 buildbot-www==2.8.2 buildbot-waterfall-view==2.8.2 buildbot-console-view==2.8.2 buildbot-grid-view==2.8.2 buildbot-badges sqlalchemy

RUN useradd -r -s /bin/false buildbot

EXPOSE 9989
ENV PYTHONPATH /config/master
ENTRYPOINT ["/usr/bin/python3", "/config/master/start.py"]
CMD []
