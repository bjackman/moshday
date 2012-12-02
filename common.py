"""
helper variables/methods that are common to all modules
"""
import subprocess
import os

default_db_path = os.path.join(os.environ["HOME"], ".synchrotron.xml")

def mount(device_name, mount_point):
  return subprocess.call(["mount", device_name, mount_point])
def unmount(device_name):
  return subprocess.call(["umount", device_name])

#take a devices uuid and return the path that synchrotron will mount it to
def mount_point(uuid):
  return os.path.join(os.environ["HOME"], ".synchrotron-" + uuid)
