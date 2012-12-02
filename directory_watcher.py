"""
watch a directory (currently dummy)
"""
import database
import pyinotify

mask = pyinotify.IN_CREATE

class INotifyCallback(pyinotify.ProcessEvent):
  def process_IN_CREATE(self_event):
    print "File created: " + event.pathname

watch_manager = pyinotify.WatchManager()
handler = INotifyCallback()
notifier = pyinotify.Notifier(watch_manager, handler)

#start and stop will be passed objects from database.SyncDevice
def start(sync_device):
  print sync_device
  print "pretending to watch %s" % sync_device.sync_dir
  watch_manager.add_watch(sync_device.sync_dir, mask, rec=True)

def stop(sync_device):
  print "stopping pretending to watch %s" % sync_device.sync_dir
