"""
module for interacting with the Synchrotron "database" (which is actually just
an XML file).
"""

from lxml import etree
from lxml.etree import Element, ElementTree
import os

default_database_path = os.path.join(os.environ["HOME"], ".synchrotron.xml")

#In this module "devices" are represented by a (uuid, sync dir) tuple.
class SyncFile(object):
  def __init__(self, filename, sync_time):
    self.filename = filename
    self.sync_time = sync_time

class SyncDevice(object):
  def __init__(self, uuid, sync_dir):
    self.files = []
    self.uuid = uuid
    self.sync_dir = sync_dir

  def add_file(self, filename, sync_time):
    new_file = SyncFile(filename, sync_time)
    self.files.append(new_file)
    return new_file

def build_from_file(filename):
  db = Database()
  in_file = open(filename, "r")
  root = etree.parse(filename).getroot()
  device_elements = root.getchildren()
  for device_element in device_elements:
    uuid = device_element.get("uuid")
    sync_file = device_element.get("sync_file")
    new_device = db.add_device(uuid, sync_file)
    file_elements = device_element.getchildren()
    for file_element in file_elements:
      filename = file_element.get("filename")
      sync_time = file_element.get("sync_time")
      new_device.add_file(filename, sync_time)
  return db

   

class Database(object):
  def __init__(self):
    self.devices = []

  #write what's in this database object into self.xml_file
  def store(self, xml_file_name=default_database_path):
    output_file = open(xml_file_name, "w")
    root = Element("synchrotron")
    #structure the root element
    for dev in self.devices:
      devElement = Element("device")
      devElement.set("uuid", dev.uuid)
      devElement.set("sync_dir", dev.sync_dir)
      for sync_file in dev.files:
        fileElement = Element("file")
        fileElement.set("filename", sync_file.filename)
        fileElement.set("sync_time", sync_file.sync_time)
        devElement.append(fileElement)
      root.append(devElement)

    #add the root elment to a tree and write it to a file
    etree.ElementTree(root).write(output_file)
    output_file.close()

  #add a device to this database
  def add_device(self, uuid, sync_dir):
    new_device = SyncDevice(uuid, sync_dir)
    self.devices.append(new_device)
    return new_device
