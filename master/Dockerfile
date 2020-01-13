FROM opensuse/tumbleweed

RUN zypper --non-interactive --gpg-auto-import-keys ref
RUN zypper --non-interactive --gpg-auto-import-keys dup -l -y
RUN zypper --non-interactive --gpg-auto-import-keys install git gcc python3-pip python3-devel libcairo2 cairo-tools python3-cairo

RUN pip install --upgrade pip
RUN pip install pycairo requests buildbot==2.5.1 buildbot-www==2.5.1 buildbot-waterfall-view==2.5.1 buildbot-console-view==2.5.1 buildbot-grid-view==2.5.1 buildbot-badges sqlalchemy

RUN useradd -r -s /bin/false buildbot

EXPOSE 9989
ENV PYTHONPATH /config/master
ENTRYPOINT ["/usr/bin/python3", "/config/master/start.py"]
CMD []
