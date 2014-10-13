#/opt/local/bin/python2.7

import usb.core
import array


class USBDevice:

    def __init__(self, vid=0x16C0):
        #TODO check vendor name and other details to ensure we have the right device
        #TODO handle return of multiple devices
        #TODO allow user selection of device but also autoselect the best candidate
        self.device = usb.core.find(idVendor=vid)
        if self.device is None:
            raise Exception('Device not found')

    def write(self, data):
        self.device.ctrl_transfer(bmRequestType=0b00100001, bRequest=0x09, wValue=0x0300, data_or_wLength=data)

    def read(self, length=128):
        return self.device.ctrl_transfer(bmRequestType=0b10100001, bRequest=0x01, wValue=0x0300, wIndex=0,
                                         data_or_wLength=length)






avr = USBDevice()

dataIn = array.array('B', [0]*128)
dataIn[0*16+0] = 255
dataIn[0*16+1] = 0
dataIn[1*16+0] = 255
dataIn[1*16+1] = 0
dataIn[2*16+0] = 255
dataIn[2*16+1] = 0
dataIn[3*16+0] = 255
dataIn[3*16+1] = 0
dataIn[4*16+0] = 255
dataIn[4*16+1] = 0
dataIn[5*16+0] = 255
dataIn[5*16+1] = 0
dataIn[6*16+0] = 255
dataIn[6*16+1] = 0
dataIn[7*16+0] = 255
dataIn[7*16+1] = 0

#print data

# SET REPORT
avr.write(dataIn)
print avr.read()