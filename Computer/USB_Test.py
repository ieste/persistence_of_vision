#/opt/local/bin/python2.7

import usb.core

import array
import time


class USBDevice:

    def __init__(self, vid=0x16C0):
        #TODO check vendor name and other details to ensure we have the right device
        #TODO handle return of multiple devices
        #TODO allow user selection of device but also autoselect the best candidate
        self.device = usb.core.find(idVendor=vid)
        if self.device is None:
            raise Exception('Device not found.')

    def write(self, data):
        self.device.ctrl_transfer(bmRequestType=0b00100001, bRequest=0x09, wValue=0x0300, data_or_wLength=data)

    def read(self, length=128):
        return self.device.ctrl_transfer(bmRequestType=0b10100001, bRequest=0x01, wValue=0x0300, wIndex=0,
                                         data_or_wLength=length)






avr = USBDevice()

for i in range(10):
    data = array.array('B', [i]*128)

    avr.write(data)
    input = avr.read()
    for j in range(128):
        if input[j] is not data[j]:
            print "error"
            print input[j]
    print i