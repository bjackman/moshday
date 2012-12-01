#!/usr/bin/python
import sys
import usb
MASS_STORAGE_CLASS = 0x08
#method to identify whether a device is mass storage
def is_mass_storage(dev):
  if dev.bDeviceClass == MASS_STORAGE_CLASS:
    return True
  #look in all the config descriptors
  for cfgDescriptor in dev:
    #look for an interface descriptor where the interface class is right
    interfaceDescriptor \
      = usb.util.find_descriptor(cfgDescriptor,
                                 bInterfaceClass=MASS_STORAGE_CLASS)
    if interfaceDescriptor is not None:
      return  True
  #we have not found that the device we recieved is valid, so return false
  return False

#pass the above function as a custom matching function to "find"
device = usb.core.find(find_all=True, custom_match=is_mass_storage)[0]

print "device descriptor: " + str(device)
for cfgDescriptor in device:
  print "config descriptor: " + str(cfgDescriptor)
  for interfaceDescriptor in cfgDescriptor:
    print "interface descriptor: " + str(interfaceDescriptor)
    for endpointDescriptor in interfaceDescriptor:
      print "endpoint descroptor: " + str(endpointDescriptor)
      for element in endpointDescriptor.__dict__:
        sys.stdout.write(element + ": ")
        sys.stdout.write(str(getattr(endpointDescriptor, element)) + "\n")
      print("")
    print("")
