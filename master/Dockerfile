from opensuse:tumbleweed

run zypper --non-interactive --gpg-auto-import-keys ref
run zypper --non-interactive --gpg-auto-import-keys dup -l -y
run zypper --non-interactive --gpg-auto-import-keys install git gcc python3-pip python3-devel libcairo2 cairo-tools python3-cairo

run pip install --upgrade pip
run pip install pycairo requests buildbot==2.0.1 buildbot-www==2.0.1 buildbot-waterfall-view==2.0.1 buildbot-console-view==2.0.1 buildbot-grid-view==2.0.1 buildbot-badges sqlalchemy

run useradd -r -s /bin/false buildbot

expose 9989
env PYTHONPATH /config/master
entrypoint ["/usr/bin/python3", "/config/master/start.py"]
cmd []
