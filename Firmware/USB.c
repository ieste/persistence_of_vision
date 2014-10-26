

#include "USB.h"

/**
 * Used while receiving data to keep track of how many bytes still need to be
 * received (data is not necessarily all sent at once, so the 
 * usbFunctionWrite() method may be called multiple times).
 */
volatile uchar bytesRemaining;

/**
 * A temporary buffer for storing data that is sent/received over USB before
 * it is written to program memory or sent to the host.
 */
volatile uchar buffer[128];

/**
 * Stores the number of pages written during an in-progress data transfer, so
 * that when a page of data is received we can calculate which address to write
 * the data in to.
 */
volatile uint32_t pagesWritten = 0;

/**
 * Stores the number of pages that need to be written during the current data
 * transfer so that when know what all the data has been sent.
 */
volatile uint8_t numPages = 0;

/**
 * Used to store page numbers so that we can only write to specific pages 
 * rather than having to write a whole image to consecutive pages. This is used
 * to re-write bad pages (where writing failed on the first attempt).
 */
volatile uint8_t pagesToWrite[128];

/**
 * Flag to indicate whether the most recent data transfer was a "hand shake",
 * i.e. did not consist of data to be stored to program memory, but rather
 * provided information about an incoming data transfer.
 */
volatile uint8_t handshaking = 1;

/**
 * USB report descriptor - this is stored in program memory. Taken from
 * hid-data VUSB example.
 */
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


/**
 * Initialise USB communication by calling the driver's initialise function.
 */
void USB_init(void) {
    cli();
    usbInit();
    _delay_ms(200);
    sei();
}


/**
 * This function is used by the USB driver to determine how to handle a
 * USB request from the host. For more details see the documentation in 
 * usbdrv/usbdrv.h.
 */
usbMsgLen_t usbFunctionSetup(uchar data[8])
{
    // Cast data to 'usbRequest_t *' for easier access to parameters.
    usbRequest_t *request = (usbRequest_t*) data;
    
    // HID Class request
    if((request->bmRequestType & USBRQ_TYPE_MASK) == USBRQ_TYPE_CLASS) {

        // The host is requesting data.
        if(request->bRequest == USBRQ_HID_GET_REPORT) {
            
            if (handshaking) {
                // If handshaking, we send back data from the buffer rather
                // than retreiving it from program memory.
                handshaking = 0;
            } else {
                // Read in the most recent page written.
                if (numPages == 90) {
                    read_page(pagesWritten - 1, (uint8_t*)buffer);
                } else {
                    read_page(pagesToWrite[pagesWritten - 1],
                              (uint8_t*)buffer);
                }
            }
            
            // Send it to the computer for validation.
            usbMsgPtr = (int)buffer;
            return 128;
          
        // The host wants to send data.
        } else if (request->bRequest == USBRQ_HID_SET_REPORT) {
        
            bytesRemaining = 128;
            
            // Toggle LED for each page transfer so that the LED blinks
            // during data transfer.
            toggle_LED();
            
            if (pagesWritten == numPages) {
                pagesWritten = 0;
                numPages = 0;
            }
            
            return USB_NO_MSG;
        }
    }
    
    // Other types of requests (vendor) are ignored.
    return 0;
}


/**
 * This function is called when the host sends a chunk of data to the
 * device. For more information see the documentation in usbdrv/usbdrv.h.
 */
uchar usbFunctionWrite(uchar *data, uchar len)
{
    uint8_t i;
 
    // We don't want to read in more than the 128 byte limit for messages.
    if(len > bytesRemaining) len = bytesRemaining;
    
    // Store the sent data.
    for(i = 0; i < len; i++) {
        buffer[128 - bytesRemaining] = (*(data + i));
        bytesRemaining--;
    }
    
    
    // Once the whole message has been received, handle it appropriately.
    if(bytesRemaining == 0) {
        
        /**
         * If we are not waiting to write any pages, then the message is
         * signaling that the host is about to send one or more pages to be
         * written, and the first byte of this message tells us how many
         * pages will be sent. 
         */
        if (numPages == 0 && buffer[0] != 0) {
            
            handshaking = 1;
            numPages = buffer[0];
            
            /** 
             * If the host is not sending a whole image (90 pages), then it
             * will have sent a list of pages we need to write to.
             */
            if (numPages < 90) {
                for (i = 0; i < numPages; i++) {
                    pagesToWrite[i] = buffer[i];
                }
            }
            
        } else {
            
            // Write the data in buffer to the appropriate location.
            if (numPages == 90) {
                write_page(pagesWritten, (uint8_t*)buffer);
            } else {
                write_page(pagesToWrite[pagesWritten], (uint8_t*)buffer);
            }
            
            pagesWritten++;
        }
        
        // Ensure the indicator LED is on at the end of a data transfer.
        if (pagesWritten == numPages) {
            LED_on();
        }
        
        // Return 1 to signal end of transfer.
        return 1;
    }
    
    return 0;
}

