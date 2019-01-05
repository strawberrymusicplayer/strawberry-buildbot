import os
import pwd
import shutil
import subprocess

WORKERNAME = open('/worker-name').read().strip()
BASEDIR = os.path.join('/persistent-data', WORKERNAME)

pwd_entry = pwd.getpwnam('buildbot')
creating_basedir = False

# Create the BASEDIR if it doesn't exist.
if not os.path.exists(BASEDIR):
  os.mkdir(BASEDIR)
  os.chown(BASEDIR, pwd_entry.pw_uid, pwd_entry.pw_gid)
  creating_basedir = True

  if os.path.exists('/first-time-setup.sh'):
    try:
      stdout = subprocess.check_output(['/bin/sh', '/first-time-setup.sh'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
      shutil.rmtree(BASEDIR)
      raise

    with open(os.path.join(BASEDIR, 'first-time-setup.log'), 'w') as fh:
      fh.write(stdout)

# Change to the buildbot user.
os.setgid(pwd_entry.pw_gid)
os.setuid(pwd_entry.pw_uid)
os.environ['HOME'] = pwd_entry.pw_dir

if creating_basedir:
  os.symlink('/config/worker/buildbot.tac', os.path.join(BASEDIR, 'buildbot.tac'))
  os.symlink('/config/worker/info', os.path.join(BASEDIR, 'info'))
  shutil.copytree('/config/dist', os.path.join(BASEDIR, 'dist'))
  #shutil.symlink('/config/mxe', os.path.join(BASEDIR, 'mxe2'))

pidfile = os.path.join(BASEDIR, 'twistd.pid')
if os.path.exists(pidfile):
  os.unlink(pidfile)

os.execlp('buildbot-worker', 'buildbot-worker', 'start', '--nodaemon', BASEDIR)
