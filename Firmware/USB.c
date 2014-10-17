
#include "USB.h"

volatile uchar bytesRemaining;
volatile uchar buffer[128];

volatile uint32_t pagesWritten = 0;
volatile uint8_t numPages = 0;
volatile uint8_t pagesToWrite[128];
volatile uint8_t handshaking = 1;

/* USB report descriptor - this is stored in program memory. Taken from
 * hid-data VUSB example. */
PROGMEM const char usbHidReportDescriptor[22] = {
    0x06, 0x00, 0xff,              // USAGE_PAGE (Generic Desktop)
    0x09, 0x01,                    // USAGE (Vendor Usage 1)
    0xa1, 0x01,                    // COLLECTION (Application)
    0x15, 0x00,                    // LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x00,              // LOGICAL_MAXIMUM (255)
    0x75, 0x08,                    // REPORT_SIZE (8)
    0x95, 0x80,                    // REPORT_COUNT (128)
    0x09, 0x00,                    // USAGE (Undefined)
    0xb2, 0x02, 0x01,              // FEATURE (Data,Var,Abs,Buf)
    0xc0                           // END_COLLECTION
};


usbMsgLen_t usbFunctionSetup(uchar data[8])
{
    // Cast data to 'usbRequest_t *' for easier access to parameters.
    usbRequest_t * request = (usbRequest_t *) data;
    
    // HID Class request
    if((request->bmRequestType & USBRQ_TYPE_MASK) == USBRQ_TYPE_CLASS) {

        // The host wants to receive data
        if(request->bRequest == USBRQ_HID_GET_REPORT) {
            
            // Read in most recent page written
            if (handshaking) handshaking = 0;
            else read_page(pagesWritten - 1, (uint8_t*)buffer);
            
            // Send it to the computer for validation
            usbMsgPtr = (int)buffer;
            return 128;
          
        // The host wants to send data.
        } else if (request->bRequest == USBRQ_HID_SET_REPORT) {
        
            bytesRemaining = 128;
            toggleLED();
            
            if (pagesWritten == numPages) {
                pagesWritten = 0;
                numPages = 0;
            }
            
            return USB_NO_MSG;
        }
    }
    
    // Other types of requests (vendor) are ignored
    return 0;
}


/* usbFunctionWrite() is called when the host sends a chunk of data to the
 * device. For more information see the documentation in usbdrv/usbdrv.h.
 */
uchar usbFunctionWrite(uchar *data, uchar len)
{
    uchar i;
    
    if(len > bytesRemaining) len = bytesRemaining;
    
    for(i = 0; i < len; i++) {
        buffer[128 - bytesRemaining] = (*(data + i));
        bytesRemaining--;
    }
    
    if(bytesRemaining == 0) {
        
        if (numPages == 0 && buffer[0] != 0) {
            
            handshaking = 1;
            numPages = buffer[0];
            
            if (numPages < 90) {
                for (i = 0; i < numPages; i++) {
                    pagesToWrite[i] = buffer[i];
                }
            }
        } else {
            if (numPages == 90) {
                write_page(pagesWritten, (uint8_t*)buffer);
            } else {
                write_page(pagesToWrite[pagesWritten], (uint8_t*)buffer);
            }
            pagesWritten++;
        }
        
        if (pagesWritten == numPages) {
            LEDon();
        }
        
        return 1;   // end of transfer
    }
    
    return 0;
}

