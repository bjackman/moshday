"""
for testing: takes a device file and a directory then syncs the directory
to the device
"""
import subprocess
import os
import sys
from stat import ST_MTIME

import pyudev

import database
from database import Database
from common import default_db_path


dev_name = sys.argv[1]
sync_dir = sys.argv[2]

#takes a device, mounts it, returns the mount point or none
def mount(device):
  device_name = device["DEVNAME"]
  uuid = device["ID_FS_UUID"]
  home = os.environ["HOME"]
  mount_point = os.path.join(home, "." + "synchrotron-" + uuid)
  if not os.path.exists(mount_point):
    os.mkdir(mount_point)
  return_code = subprocess.call(["mount", device_name, mount_point])
  if return_code == 0:
    return mount_point
  else:
    return None

#unmounts a device
def unmount(device):
  device_name = device["DEVNAME"]
  return_code = subprocess.call(["umount", device_name])

#takes a device name and returns where it is mounted to
def dev_mounted_at(device_name):
  mount_process = subprocess.Popen("mount", stdout=subprocess.PIPE)
  lines = mount_process.communicate()[0].split("\n")
  for line in lines:
    if device_name in line:
      return line.split()[2]
  return None

#get a udev object for the device
context = pyudev.Context()
device = None
for partition in context.list_devices(subsystem="block", 
                                      DEVTYPE="partition"):
  if partition["DEVNAME"] == dev_name:
    device = partition
  
if device is None:
  print "could not find %s\n" % dev_name
  sys.exit()

uuid = device["ID_FS_UUID"]
if dev_mounted_at(dev_name) is not None:
  print "%s is mounted." % dev_name
  sys.exit()

mount_point = mount(device)
print mount_point
filenames = os.listdir(mount_point)
filepaths = map(lambda s: os.path.join(mount_point, s), filenames)
file_tuples = zip(filenames, filepaths)

db = Database()
db_dev = db.add_device(uuid, sync_dir)
for file_tuple in file_tuples:
  filename = file_tuple[0]
  filepath = file_tuple[1]
  modify_time = str(os.stat(filepath)[ST_MTIME])
  db_dev.add_file(filename, modify_time)
db.store(default_db_path)

unmount(device)
