#!/usr/bin/python
"""
detects udev events regarding appearance and disappearance of "partition" devs
"""
import pyudev
from pyudev import Context, Monitor
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by("block", device_type="partition")
monitor.start()
for device in iter(monitor.poll, None):
  if "DEVNAME" in device:
    print "Device %s %sd" % (device["DEVNAME"], device.action)
  else:
    print "Event recieved - no device name available"
