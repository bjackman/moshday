import pyudev
from pyudev import Context
context = Context()

available_partitions = []

def get_partitions():
  return_list = []
  for partition in context.list_devices(subsystem="block", DEVTYPE="partition"):
    return_list.append(device)
  return return_list

available_partitions = get_partitions()

print "Enter the number next to the device you would like to use."
for i in range(len(available_partitions)):
  print "%d: %s", (i, partition["DEVNAME"])

partition = partitions(int(raw_input()))


