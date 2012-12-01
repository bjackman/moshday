#!/usr/bin/python
#for linux: adding a new interface to the database
import subprocess
import sys
import os

import pyudev
from pyudev import Context
context = Context()

available_partitions = []

def get_partitions():
  return_list = []
  for partition in context.list_devices(subsystem="block", DEVTYPE="partition"):
    return_list.append(partition)
  return return_list

#takes a device name and returns where it is mounted to
def dev_mounted_at(device_name):
  mount_process = subprocess.Popen("mount", stdout=subprocess.PIPE)
  lines = mount_process.communicate()[0].split("\n")
  for line in lines:
    if device_name in line:
      return line.split()[2]
  return None

#takes a device name, mounts it, returns the mount point or none
def mount(device):
  device_name = device["DEVNAME"]
  uuid = device["ID_FS_UUID"]
  home = os.environ["HOME"]
  mount_point = os.path.join(home, "." + "synchrotron-" + uuid)
  if not os.path.exists(mount_point):
    os.mkdir(mount_point)
  mount_process = subprocess.Popen(["mount", device_name, mount_point])
  mount_process.communicate()
  if mount_process.returncode == 0:
    return mount_point
  else:
    return None
  

available_partitions = get_partitions()

#choose which partition to sync
print "Enter the number next to the device you would like to use."
for i in range(len(available_partitions)):
  print "%d: %s" % (i, available_partitions[i]["DEVNAME"])

partition = available_partitions[int(raw_input())]
device_name = partition["DEVNAME"]

#complain if the partition is already mounted 

mount_point = dev_mounted_at(device_name)
if mount_point is not None:
  sys.stderr.write("Device %s is mounted at %s - unmount to continue\n"
                   % (device_name, mount_point))
  sys.exit()

uuid = partition["ID_FS_UUID"]

print mount(partition)
