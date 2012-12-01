#!/usr/bin/python
import subprocess
import sys
import pyudev
from pyudev import Context
context = Context()

available_partitions = []

def get_partitions():
  return_list = []
  for partition in context.list_devices(subsystem="block", DEVTYPE="partition"):
    return_list.append(partition)
  return return_list

#for LINUX: takes a device name and returns where it is mounted to
def dev_mount_point(device_name):
  mount_process = subprocess.Popen("mount", stdout=subprocess.PIPE)
  lines = mount_process.communicate()[0].split("\n")
  for line in lines:
    print "searching for \"%s\" in: %s" % (device_name, line)
    if device_name in line:
      return line.split()[2]
  return None

available_partitions = get_partitions()

#choose which partition to sync
print "Enter the number next to the device you would like to use."
for i in range(len(available_partitions)):
  print "%d: %s" % (i, available_partitions[i]["DEVNAME"])

partition = available_partitions[int(raw_input())]
device_name = partition["DEVNAME"]

#complain if the partition is already mounted 

mount_point = dev_mount_point(device_name)
if mount_point is not None:
  sys.stderr.write("Device % is mounted at %s - unmount to continue\n"
                   % (device_name, mount_point))
  sys.exit()
else:
  print "ok, not mounted"
