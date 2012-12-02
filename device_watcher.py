"""
detects appearance of mass storage devices, and if they are mapped in the
database starts the daemon to watch their 
"""
import os
import sys
import pyudev
from pyudev import Context, Monitor
import database
from database import Database
from common import default_db_path
import directory_watcher

#if no database
if not os.path.isfile(default_db_path):
  sys.stderr.write("could not find database at %s.\n" % default_db_path)
  sys.exit()
#if database is an empty file
elif os.stat(default_db_path)[6]==0:
  sys.stderr.write("database file at %s is empty.\n" % default_db_path)
  sys.exit()
else:
  db = database.build_from_file(default_db_path)

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by("block", device_type="partition")
monitor.start()
#watch forever for new devices
#this seems to return a tuple and not a Device.. strange
for device_tuple in monitor:
  action = device_tuple[0]
  device = device_tuple[1]
  if action == "add":
    if device["ID_FS_UUID"] in db.devices:
      directory_watcher.start(db.devices[device["ID_FS_UUID"]])
    else:
      print "device %s inserted, not synced." % device["DEVNAME"]
  elif action == "remove":
    if device["ID_FS_UUID"] in db.devices:
      directory_watcher.stop(db.devices[device["ID_FS_UUID"]])
    else:
      print "device %s removed, not synced." % device["DEVNAME"]
    
