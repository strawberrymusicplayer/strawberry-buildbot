from opensuse:tumbleweed

run zypper --non-interactive --gpg-auto-import-keys ref
run zypper --non-interactive --gpg-auto-import-keys dup -l -y
run zypper --non-interactive --gpg-auto-import-keys install git gcc python3-pip python3-devel libcairo2 cairo-tools python3-cairo

run pip install --upgrade pip
run pip install pycairo requests buildbot==1.6.0 buildbot-www==1.6.0 buildbot-waterfall-view==1.6.0 buildbot-console-view==1.6.0 buildbot-grid-view==1.6.0 buildbot-badges sqlalchemy

run useradd -r -s /bin/false buildbot

expose 9989
env PYTHONPATH /config/master
entrypoint ["/usr/bin/python3", "/config/master/start.py"]
cmd []
