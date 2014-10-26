"""
Extension of the PyUSB library to provide functionality for USB communication
via HID control transfers.

USBDevice -- represents an external USB device we wish to communicate with.
    write_pages -- writes a number of pages to the USB device.
"""

# Import USB functionality from PyUSB library.
import usb.core

# Import other utilities.
import array
import time


class USBDevice:

    def __init__(self, vid=0x16C0, view=None):

        # Try to locate a device with the provided vendor ID.
        self.device = usb.core.find(idVendor=vid)
        self.view = view

        # If no device can be located, output throw error or display in the status bar.
        if self.device is None:
            if view is None:
                raise Exception('Device not found.')
            else:
                self.view.statusbar_text('USB Device not found.')

    def _write(self, data):

        # Make a data out control transfer.
        self.device.ctrl_transfer(bmRequestType=0b00100001, bRequest=0x09, wValue=0x0300, data_or_wLength=data)

    def _read(self, length=128):

        # Make a data in control transfer.
        return self.device.ctrl_transfer(bmRequestType=0b10100001, bRequest=0x01, wValue=0x0300, wIndex=0,
                                         data_or_wLength=length)

    def write_pages(self, data):
        """
        Write image data to a USB device.
        An image consists of 90 x 128 byte pages. Each page is read back and validated after writing.
        If a page has failed to write, a re-write will be attempted three times before aborting.

        :param data: an array of 90 pages of data (each page being an array of 128 bytes) to be written.
        """
        try:
            # If no USB device is connected, do not attempt to write data.
            if self.device is None or self.view is None:
                return

            # Keeps track of the pages which failed to write.
            failed = []

            # A handshake indicating we want to send 90 pages of data.
            handshake = array.array('B', [90] + [0]*127)

            # Send and receive handshake
            self._write(handshake)
            self.view.statusbar_text("Writing to AVR...")

            # Send each of the pages, with a brief delay between each, and keep track of pages which are incorrect
            for i in range(len(data)):
                time.sleep(0.1)
                self._write(data[i])
                written = self._read()
                for j in range(128):
                    if written[j] is not data[i][j]:
                        failed.append(i)
                        break

            # Try three times to write any failed pages
            tries = 0
            while len(failed):
                if tries > 3:
                    break
                pages = failed[:]
                failed = []

                # Send and receive a handshake indicating which pages we are re-writing.
                handshake = array.array('B', [len(pages)] + pages + [0]*(127-len(pages)))
                self._write(handshake)

                # Attempt to write and validate failed pages.
                for i in pages:
                    time.sleep(0.1)
                    self._write(data[i])
                    written = self._read()
                    for j in range(128):
                        if written[j] is not data[i][j]:
                            failed.append(i)
                            break

                tries += 1

            # Indicate success or failure in the status bar.
            if len(failed) is not 0:
                self.view.statusbar_text("Writing failed after 3 attempts. Aborted.")
            else:
                self.view.statusbar_text("Transfer succeeded.")

        # Notify user if USB gets disconnected.
        except usb.USBError:
            self.view.statusbar_text("USB connection failed.")
            return