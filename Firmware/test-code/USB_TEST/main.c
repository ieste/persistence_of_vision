/*
*   main.c
*   Created by Isabella Stephens on 9/09/2014.
*
*   For the ATMega328P
*
*   PD2 (INT0)  D+  Green
*   PD4         D-  White
*
*/

#define F_CPU 16000000UL     // 16 MHz

// Includes relevant libraries
#include <avr/io.h>
#include <avr/interrupt.h>  /* for sei() */
#include <util/delay.h>     /* for _delay_ms() */
#include <avr/pgmspace.h>   /* required by usbdrv.h */

//#include <avr/eeprom.h>

#include "usbdrv.h"

#define uchar unsigned char

#define LATCH 3     // Green
#define CLOCK 4     // Yellow
#define DATA 5      // Blue
#define FET2 2      // White
#define FET1 1      // White
#define ENABLE 0
#define SHIFT_REG PORTC
#define SHIFT_DIR DDRC

void clockInit(void);
void clockInitBAM(void);
void shift_data_in (uchar data);
void toggle_latch (void);
void ledInit(void);

volatile uchar flag;
volatile uchar fet;
volatile uchar bytesRemaining;
volatile uchar ds[4][32];
volatile uchar dsh[32] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255,
    170, 170, 170, 170, 204, 204, 204, 204, 240, 240, 240, 240, 0, 255, 0, 255};
volatile uchar dataSet;


int main(void)
{

    usbInit();      // Initialise USB

    ledInit();      // Initialise the shift registers and mosfets
    
    //clockInit();    // Set up clock interrupts for PWM
    clockInitBAM();
    
    sei();          // Enable interrupts
    
    dataSet = 0;
    flag = 0;
    fet = 0;

    while(1) {  // Main loop
        usbPoll();
        
    }
}


ISR(TIMER1_COMPA_vect)
{
    
    flag &= 7; // If flag reaches 8, reset it to 0.
    
    //shift_data_in(ds[0][flag*2 + fet]);

    shift_data_in(dsh[flag*4 + fet*2 + 1]);
    shift_data_in(dsh[flag*4 + fet*2]);
    /*
    if (fet) {
        shift_data_in(255);
        shift_data_in(255);
        
    } else {
        shift_data_in(0);
        shift_data_in(0);
        
    }
    */
    
    // Toggle the mosfets and latch. - should happen at the same time as the latch
    SHIFT_REG ^= (1 << FET1) | (1 << FET2) | (1 << LATCH);
    toggle_latch();
    
    
    
    fet ^= 1;
    flag += fet;
    if (fet) OCR1A <<= 1;
    //if (flag == 8) OCR1A = 1;
    if (~OCR1A) OCR1A <<= 1;
}

//interrupt service routine for timer
/*
ISR(TIMER1_COMPA_vect, ISR_NOBLOCK)
{
    if (bytesRemaining != 0) return;
    if (dataSet == 0) {
        shift_data_in(0);
        toggle_latch();
        toggle_latch();
        return;
    }
    
    //PORTD |= 1;
    
    
    //if (ds[flag*2 + fet] == 0) PORTD |= 1;
    if (flag == 8) flag = 0;
    
    //toggle_latch();
    //shift_data_in(d[fet][flag]);

    //shift_data_in(ds[0][flag*2 + fet]);
    shift_data_in(ds[flag][fet]);
    
    // Toggle the mosfets and latch. - should happen at the same time as the latch
    SHIFT_REG ^= (1 << FET1) | (1 << FET2) | (1 << LATCH);
    toggle_latch();
    
    fet ^= 1;
    flag += fet;
}
 */

void ledInit(void) {
    // Set the Latch, Clock and Data lines as outputs.
    SHIFT_DIR |= (1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << FET1) |
    (1 << FET2) | (1 << ENABLE);
    
    // Set the Latch, Clock and Data lines low. Also MOSFET 2.
    SHIFT_REG &= ~((1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << FET2)
                   | (1 << ENABLE));
    
    // Set MOSFET 1 high.
    SHIFT_REG |= (1 << FET1);
    
    //DDRD |= 1;
    //PORTD &= ~(1);
}


usbMsgLen_t usbFunctionSetup(uchar data[8])
{
    // Cast data to 'usbRequest_t *' for a more user-friendly access to parameters
    usbRequest_t * request = (usbRequest_t *) data;
    
    // HID Class request
    if((request->bmRequestType & USBRQ_TYPE_MASK) == USBRQ_TYPE_CLASS) {
        
        if(request->bRequest == USBRQ_HID_GET_REPORT) {
            // The host wants to send data
            
            //
            bytesRemaining = 128;
            
            return USB_NO_MSG;
            // Implement differently???
            
        } else if (request->bRequest == USBRQ_HID_SET_REPORT) {
            // The host wants to receive data
            
            // Consider not implementing sending of data, although it is
            // useful for testing and validation to begin with.
            
            // Some code
            bytesRemaining = 128;
            // change??
            
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


/* USB report descriptor - this is stored in program memory?? */

PROGMEM const char usbHidReportDescriptor[22] = {
    0x06, 0x00, 0xff,              // USAGE_PAGE (Generic Desktop)
    0x09, 0x01,                    // USAGE (Vendor Usage 1)
    0xa1, 0x01,                    // COLLECTION (Application)
    0x15, 0x00,                    //   LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x00,              //   LOGICAL_MAXIMUM (255)
    0x75, 0x08,                    //   REPORT_SIZE (8)
    0x95, 0x80,                    //   REPORT_COUNT (128)
    0x09, 0x00,                    //   USAGE (Undefined)
    0xb2, 0x02, 0x01,              //   FEATURE (Data,Var,Abs,Buf)
    0xc0                           // END_COLLECTION
};


/* usbFunctionRead() is called when the host requests a chunk of data from
 * the device. For more information see the documentation in usbdrv/usbdrv.h.
 */
uchar usbFunctionRead(uchar *data, uchar len)
{
    uchar d1, d2, i;
    
    if(len > bytesRemaining) len = bytesRemaining;
    
    
    for(i = 0; i < len; i++) {
        d1 = 3 - (bytesRemaining-1)/32;
        d2 = 32 - (bytesRemaining - (32*(4 - d1 - 1)));
        bytesRemaining--;
        (*(data + i)) = (*(((uchar *)(*(ds + d1))) + d2));
    }

    
    return len;
}


/* usbFunctionWrite() is called when the host sends a chunk of data to the
 * device. For more information see the documentation in usbdrv/usbdrv.h.
 */
uchar usbFunctionWrite(uchar *data, uchar len)
{
    uchar d1, d2, i;
    
    if(bytesRemaining == 0) return 1;   // end of transfer
    
    if(len > bytesRemaining)len = bytesRemaining;
    
    dataSet = 1;
    
    for(i = 0; i < len; i++) {
        d1 = 3 - (bytesRemaining-1)/32;
        d2 = 32 - (bytesRemaining - (32*(4 - d1 - 1)));
        (*(((uchar *)(*(ds + d1))) + d2)) = (*(data + i));
        
        
        bytesRemaining--;
    }
    
    return bytesRemaining == 0; // return 1 if this was the last chunk
}


void
toggle_latch (void)
{
    // Delay for 100 ns to ensure latching succeeds.
    //_delay_us(0.1);
    // Toggle the latch.
    SHIFT_REG ^= (1 << LATCH);
    
    //when latch goes high switch mosfets
}


void
shift_data_in (uint8_t data)
{
    uint8_t i;
    
    for (i = 0; i < 8; i++)
    {
        if (((data >> (7 - i)) & 1))
            SHIFT_REG |= (1 << DATA);
        else
            SHIFT_REG &= (~(1 << DATA));
        
        SHIFT_REG ^= (1 << CLOCK);
       
        SHIFT_REG ^= (1 << CLOCK);
    }
}




void
clockInit (void)
{
    cli();  // disable interrupts while setting up
    TCCR1B |= (1 << CS12) | (1 << CS10);    // Divide clock by 1024
    OCR1A = 1;  // We can shift this during the ISR to do BAM
    TCCR1B |= (1 << WGM12); // Put timer into CTC mode
    TIMSK1 |= (1 << OCIE1A); // Enable the timer compare interrupt
    //sei();  // enable interrupts
}

void
clockInitBAM(void)
{
    cli();  // disable interrupts while setting up
    //TCCR1B |= (1 << CS12);    // Divide clock by 256 - may need changing if too slow
    TCCR1B |= (1 << CS12) | (1 << CS10);    // Divide clock by 1024
    OCR1A = 1;  // We can shift this during the ISR to do BAM (still set initial)
    TCCR1B |= (1 << WGM12); // Put timer into CTC mode
    TIMSK1 |= (1 << OCIE1A); // Enable the timer compare interrupt
    //sei();  // enable interrupts
}









