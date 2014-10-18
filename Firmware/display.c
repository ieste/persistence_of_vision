
#include "display.h"
#include "main.h" // needed to get mode??
#include <util/delay.h>

// Data source
// Mode 0: flash
// Test mode 1: flash
// Test mode 2: hard coded
// test mode 3: hard coded
// test mode 4: complicated

// Store whether display is on so others can access this information.

extern volatile uint8_t mode;
volatile uint16_t position = 0;
volatile uint8_t mosfet = 0;

volatile uint8_t bitPosition = 0;

void enableDisplay(void) {
    
    /*
     MATHS:
     Max speed: 250 RPM
     250/60 = 4.167 RPS
     4.16667.. * 360 = 1500 degrees/second
     1/1500 = 0.00066667 seconds per pixel
     16 delays add up to ~667 microseconds
     1+2+4+8+16+32+64+128 = 255 (shortest delay is [half of] 667/255 microseconds)
     1/1500*1000*1000/255/2 =
     Shortest delay is 1.30718 microseconds.
     
     Min speed: 60 RPM
     60/60 = 1 RPS
     1 * 360 = 360 degress/second
     1/360 = 0.00277778 seconds per pixel
     16 delays add up to ~2778 microseconds
     (shortest delay is [half of] 2778/255 microseconds)
     2778/255/2 = 5.447 microseconds.
     
     1.30718/(1/16000000*1000*1000)
     1,2,4,8,16,32,64,128
     20,40,80,160,320,640,1280,2560
     87, ..., 10240
     
     Conclusion:
     Don't use the prescaler.
     */
    
    cli();
    TCCR1B |= (1 << CS10); // Divide clock by 1
    //TCCR1B |= (1 << CS10) | (1 << CS12); // Divide by 1024
    //OCR1A = 15624; // Compare to 20
    OCR1A = 60;
    TCCR1B |= (1 << WGM12); // Put timer into CTC mode
    TIMSK1 |= (1 << OCIE1A); // Enable the interrupt
    sei();
}

void disableDisplay(void) {
    TIMSK1 &= ~(1 << OCIE1A);
}


ISR(TIMER1_COMPA_vect) {
    uint8_t data[2];

    switch (mode) {
        case 0:
        case 1:
            data[0] = read_byte(position);
            data[1] = read_byte(position + 1);
            break;
        case 2:
            data[0] = 255;
            data[1] = 255;
            break;
        case 3:
            data[0] = (mosfet << 7);
            data[1] = 0;
            break;
        case 4:
            data[0] = 0;
            data[1] = 0;
            break;
                     
    }
    
    // Display it (may need to switch these).
    // Data is displayed on the rising edge of the latch.
    shiftDataIn(data[0]);
    shiftDataIn(data[1]);
    shiftLatchFets();
    //_delay_us(1);
    shiftLatch();
    //_delay_us(1);
    
    bitPosition += mosfet;
    if(mosfet) bitPosition &= 7;
    if (bitPosition == 0) {
        OCR1A = 60;
    }
    
    OCR1A <<= mosfet;
    
    // make any modifications to the interrupt
    //OCR1A <<= mosfet;
    
    // 0, 2, 4, 8, 10, 12, 14, 16
    // 18 20 22 24 26 28 30 32
    position += 2;
    //if (~(position % 34)) OCR1A = 20;
    
    if (position == 2880) position = 0;
    
    mosfet ^= 1;
}