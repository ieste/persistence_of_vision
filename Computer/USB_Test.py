#/opt/local/bin/python2.7
#

import usb.core
import usb.util
import usb.control

# find our device
dev = usb.core.find(idVendor = 0x16c0)

# was it found?
if dev is None:
    raise ValueError('PoV Device not found')

#print dev

#data = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
#print data[11]

# SET REPORT
#dev.ctrl_transfer(bmRequestType=0b00100001, bRequest=0x09, wValue=0x0300, data_or_wLength=129)

# GET REPORT
array = dev.ctrl_transfer(bmRequestType=0b10100001, bRequest=0x01, wValue=0x0300, wIndex=0, data_or_wLength=129)
print array[5]

#print dev









class USBInterface:
    VENDOR_ID = 0x16C0

    def __init__(self):
        device = usb.core.find(idVendor = self.VENDOR_ID)
        if device is None:
            raise Exception('Device not found')



"""

dev1 =

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
ep.write('test')
"""

"""
import usb
import usb.core
import usb.util


dev = usb.core.find(idVendor=0x16c0, idProduct=0x05df)

if dev is None:
    raise ValueError('Device not found.')
dev.set_configuration()

msg = 'test'
print dev.ctrl_transfer(32, 9, 0, 0, msg)
"""


"""


class _DeviceDescriptor(object):
    def __init__(self, idVendor, idProduct):
        self.bLength = 18
        self.bDescriptorType = usb.util.DESC_TYPE_DEVICE
        self.bcdUSB = 0x0200
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.bcdDevice = 0x0001
        self.iManufacturer = 0
        self.iProduct = 0
        self.iSerialNumber = 0
        self.bNumConfigurations = 0
        self.bMaxPacketSize0 = 64
        self.bDeviceClass = 0xff
        self.bDeviceSubClass = 0xff
        self.bDeviceProtocol = 0xff
        self.bus = 1
        self.address = 1
        self.port_number= None

# We are only interested in test usb.find() function, we don't need
# to implement all IBackend stuff
class _MyBackend(usb.backend.IBackend):
    def __init__(self):
        self.devices = [_DeviceDescriptor(devinfo.ID_VENDOR, p) for p in range(4)]
    def enumerate_devices(self):
        return range(len(self.devices))
    def get_device_descriptor(self, dev):
        return self.devices[dev]

class FindTest(unittest.TestCase):
    def test_find(self):
        b = _MyBackend()
        self.assertEqual(find(backend=b, idVendor=1), None)
        self.assertNotEqual(find(backend=b, idProduct=1), None)
        self.assertEqual(len(tuple(find(find_all=True, backend=b))), len(b.devices))
        self.assertEqual(len(tuple(find(find_all=True, backend=b, idProduct=1))), 1)
        self.assertEqual(len(tuple(find(find_all=True, backend=b, idVendor=1))), 0)

        self.assertEqual(
                len(tuple(find(
                        find_all=True,
                        backend=b,
                        custom_match = lambda d: d.idProduct==1))),
                    1)

        self.assertEqual(
                len(tuple(
                    find(
                        find_all=True,
                        backend=b,
                        custom_match = lambda d: d.idVendor==devinfo.ID_VENDOR,
                        idProduct=1))),
                    1)

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FindTest))
    return suite

if __name__ == '__main__':
    utils.run_tests(get_suite())

"""

"""
b = libusb1.get_backend()
if b is None:
    print('failed')
"""

"""
dev = usb.core.find(idVendor=0x16c0, idProduct=0x05df)

if dev is None:
    raise ValueError('Device not found.')
dev.set_configuration()

msg = 'test'
print dev.ctrl_transfer(32, 9, 0, 0, msg)
"""