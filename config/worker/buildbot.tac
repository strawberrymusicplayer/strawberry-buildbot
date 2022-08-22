
import os
import json

from buildbot_worker.bot import Worker
from twisted.application import service

application = service.Application('buildbot-worker')
workername = open('/worker-name').read().strip()
basedir = os.path.join('/persistent-data', workername)
PASSWORDS = json.load(open('/config/secret/passwords.json'))

rotateLength = 10000000
maxRotatedFiles = 10

from twisted.python.logfile import LogFile
from twisted.python.log import ILogObserver, FileLogObserver
logfile = LogFile.fromFullPath(os.path.join(basedir, "twistd.log"), rotateLength=rotateLength, maxRotatedFiles=maxRotatedFiles)
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

buildmaster_host = 'master'
port = 9989
passwd = PASSWORDS[workername]
keepalive = 600
umask = 0o22
maxdelay = 300
numcpus = None
allow_shutdown = None
maxretries = None

s = Worker(buildmaster_host, port, workername, passwd, basedir, keepalive, umask=umask, maxdelay=maxdelay, numcpus=numcpus, allow_shutdown=allow_shutdown, maxRetries=maxretries)
s.setServiceParent(application)
