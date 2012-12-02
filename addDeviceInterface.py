#!/usr/bin/python
#for linux: adding a new interface to the database
#takes the directory to be synced as an argument
import subprocess
import sys
import os
from ctypes import cdll

import pyudev
from pyudev import Context

if len(sys.argv) < 2:
  print "Please proved the directory you want to sync as an argument."
  sys.exit()

sync_dir = sys.argv[1]
if not os.path.exists(sync_dir):
  print("Specified sync path does not exist. Create it? (y/n)")
  if (raw_input() == "y"):
    try:
      os.makedirs(sync_dir)
    except e:
      print "could not create that directory:"
      print str(e)
      sys.exit()

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
  return_code = subprocess.call(["mount", device_name, mount_point])
  if return_code == 0:
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

if mount(partition) is None:
  print "Couldn't mount your device. Please run me as root!"
  sys.exit()
