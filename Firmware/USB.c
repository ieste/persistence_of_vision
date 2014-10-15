

#include "USB.h"
//#include "usbdrv/usbdrv.h"

volatile uchar bytesRemaining;
volatile uchar buffer[128];
volatile uint32_t pagesWritten = 0;

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
        
        if(request->bRequest == USBRQ_HID_GET_REPORT) {
            // The host wants to receive data
            
            // Consider not implementing sending of data, although it is
            // useful for testing and validation to begin with.
            
            // Populate buffer with the contents of the current page
            
            // read in most recent page written
            read_page(pagesWritten - 1, (uint8_t*)buffer);
            
            
            //
            //bytesRemaining = 128;
            
            // implement differently?
            //return USB_NO_MSG;
            
            usbMsgPtr = (int)buffer;
            return 128;
          
            
        } else if (request->bRequest == USBRQ_HID_SET_REPORT) {
            // The host wants to send data
        
            bytesRemaining = 128;
            toggleLED();
            
            return USB_NO_MSG;
        }
    }
    
    // Other types of requests (vendor) are ignored
    return 0;
    
    /*
     * If the SETUP indicates a control-in transfer, you should provide the
     * requested data to the driver. There are two ways to transfer this data:
     * (1) Set the global pointer 'usbMsgPtr' to the base of the static RAM data
     * block and return the length of the data in 'usbFunctionSetup()'. The driver
     * will handle the rest. Or (2) return USB_NO_MSG in 'usbFunctionSetup()'. The
     * driver will then call 'usbFunctionRead()' when data is needed. See the
     * documentation for usbFunctionRead() for details. */
    // If not using usbFunctionRead() disable it in the usbconfig.
    
    /*
     * If the SETUP indicates a control-out transfer, the only way to receive the
     * data from the host is through the 'usbFunctionWrite()' call. If you
     * implement this function, you must return USB_NO_MSG in 'usbFunctionSetup()'
     * to indicate that 'usbFunctionWrite()' should be used. See the documentation
     * of this function for more information. If you just want to ignore the data
     * sent by the host, return 0 in 'usbFunctionSetup()'. */
}





/* usbFunctionRead() is called when the host requests a chunk of data from
 * the device. For more information see the documentation in usbdrv/usbdrv.h.
 */
/*
uchar usbFunctionRead(uchar *data, uchar len)
{
    uchar i;
    
    if(len > bytesRemaining) len = bytesRemaining;
    
    for(i = 0; i < len; i++) {
        (*(data + i)) = buffer[128 - bytesRemaining];
        bytesRemaining--;
    }
    
    return len;
}
*/

/* usbFunctionWrite() is called when the host sends a chunk of data to the
 * device. For more information see the documentation in usbdrv/usbdrv.h.
 */
uchar usbFunctionWrite(uchar *data, uchar len)
{
    uchar i;
    
    if(len > bytesRemaining)len = bytesRemaining;
    
    for(i = 0; i < len; i++) {
        buffer[128 - bytesRemaining] = (*(data + i));
        bytesRemaining--;
    }
    
    if(bytesRemaining == 0) {
        
        write_page(pagesWritten, (uint8_t*)buffer);
        pagesWritten++;
        
        return 1;   // end of transfer
    }
    
    return 0;
}

