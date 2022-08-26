FROM opensuse/leap:15.4

RUN zypper -n ar -c -f -n 'repo-python' https://download.opensuse.org/repositories/devel:/languages:/python/15.4/ repo-python

RUN zypper --non-interactive --gpg-auto-import-keys ref
RUN zypper --non-interactive --gpg-auto-import-keys up -l -y
RUN zypper --non-interactive --gpg-auto-import-keys install shadow git python3-pip python3-devel python3-cairo python3-wheel python3-requests python3-SQLAlchemy python3-service_identity

RUN pip3 install --upgrade pip
RUN pip3 install buildbot==3.6.0 buildbot-www==3.6.0 buildbot-waterfall-view==3.6.0 buildbot-console-view==3.6.0 buildbot-grid-view==3.6.0 buildbot-badges

RUN useradd -r -s /bin/false buildbot

EXPOSE 9989
ENV PYTHONPATH /config/master
ENTRYPOINT ["/usr/bin/python3", "/config/master/start.py"]
CMD []
