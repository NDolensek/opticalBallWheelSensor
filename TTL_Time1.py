#!/usr/bin/python
import sys
import usb.core
import usb.util
import time
import RPi.GPIO as GPIO

endTime = input("How long is the imaging session (answer in seconds and press ENTER; time from TTL HIGH to end of the aqusition)?")

dev = usb.core.find(idVendor=0x046d, idProduct=0xc332) #Logitech G502 Proteus Spectrum mouse

# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]
# if the OS kernel already claimed the device, which is most likely true
# thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
if dev.is_kernel_driver_active(interface) is True:
  # tell the kernel to detach
  dev.detach_kernel_driver(interface)
  # claim the device
  usb.util.claim_interface(dev, interface)




GPIO.setmode(GPIO.BCM) #sets processor GPIO numbering sys (GPIO No.)
GPIO.setup(21, GPIO.IN) #sets pin GPIO 21 as input

pinVal = GPIO.input(21)

while pinVal == 0:
  pinVal = GPIO.input(21)

startTime = time.time()
timestamp = 0
  
while timestamp < endTime:
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        timestamp = time.time() - startTime
        print(timestamp, "," , data)
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue



# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)



GPIO.cleanup()