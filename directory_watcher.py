"""
Spawns a thread which watches directories and calls a callback on events.
Pass an instance of database.SyncDevice to start() to begin watching that
device's sync directory (the device must already be in the database)
"""
import database
import pyinotify

mask = pyinotify.IN_CREATE

class INotifyCallback(pyinotify.ProcessEvent):
  def process_IN_CREATE(self, event):
    print "File created: " + event.pathname

class DirectoryWatcher(object):
  def __init__(self):
    self.watch_manager = pyinotify.WatchManager()
    self.handler = INotifyCallback()
    self.notifier = pyinotify.ThreadedNotifier(self.watch_manager, 
                                               self.handler)
    self.notifier.start()
    #dict where key is watch directory and value is a watch descriptor
    #(used to remove a watch)
    self.watch_descriptors = {}

  #start and stop will be passed objects from database.SyncDevice
  def start(self, sync_device):
    print "pretending to watch %s" % sync_device.sync_dir
    wd = self.watch_manager.add_watch(sync_device.sync_dir, mask, rec=True)
    #append new watch descriptors into dictionary
    self.watch_descriptors = dict(self.watch_descriptors.items() + wd.items())

  def stop(self, sync_device):
    #only stop watching the device if we were currently watching it!
    if sync_device.sync_dir in self.watch_descriptors:
      print "stopping pretending to watch %s" % sync_device.sync_dir
      wd = self.watch_descriptors[sync_device.sync_dir]
      self.watch_manager.rm_watch(wd, rec=True)
