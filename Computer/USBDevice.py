#/opt/local/bin/python2.7

import usb.core

import array
import time


from PIL import Image


class USBDevice:

    #TODO Error handling in case of: "USBError: [Errno None] libusb0-dll:err [control_msg] sending control message failed, win error: A device attached to the system is not functioning."


    def __init__(self, vid=0x16C0, view=None):
        #TODO check vendor name and other details to ensure we have the right device
        #TODO handle return of multiple devices
        #TODO allow user selection of device but also auto-select the best candidate
        self.device = usb.core.find(idVendor=vid)
        if self.device is None:
            if view is None:
                raise Exception('Device not found.')
            else:
                view.statusbar_text('USB Device not found.')

    def _write(self, data):
        self.device.ctrl_transfer(bmRequestType=0b00100001, bRequest=0x09, wValue=0x0300, data_or_wLength=data)

    def _read(self, length=128):
        return self.device.ctrl_transfer(bmRequestType=0b10100001, bRequest=0x01, wValue=0x0300, wIndex=0,
                                         data_or_wLength=length)

    def write_pages(self, data):

        failed = []
        handshake = array.array('B', [90] + [0]*127)

        # send and receive handshake
        self._write(handshake)
        print "Writing " + str(self._read()[0]) + " page(s)..."
        UI.statusbar_text("Writing " + str(self._read()[0]) + " page(s)...")

        for i in range(len(data)):
            time.sleep(0.1)
            self._write(data[i])
            written = self._read()
            for j in range(128):
                if written[j] is not data[i][j]:
                    failed.append(i)
                    break

        tries = 0;
        while len(failed):
            if tries > 3:
                break
            print "Failed pages:", failed, ". Resending..."
            pages = failed[:]
            failed = []
            handshake = array.array('B', [len(pages)] + pages + [0]*(127-len(pages)))

            #send and receive handshake
            self._write(handshake)
            print "Writing", self._read()[0], "page(s)..."

            for i in pages:
                time.sleep(0.1)
                self._write(data[i])
                written = self._read()
                print written
                print data[i]
                for j in range(128):
                    if written[j] is not data[i][j]:
                        failed.append(i)
                        break

            # will repeat until all pages are successfully written.
            tries += 1

        if len(failed) is not 0:
            print "Writing to pages", failed, "failed after 3 attempts. Aborted."
        else:
            print "Transfer succeeded."