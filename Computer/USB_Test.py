
import usb.core
import usb.util


from array import *

dev = usb.core.find(idVendor=0x16c0, idProduct = 0x05df)

if dev is None:
    raise ValueError('Device not found.')
dev.set_configuration()

msg = 'test'
print dev.ctrl_transfer(32, 9, 0, 0, msg)
