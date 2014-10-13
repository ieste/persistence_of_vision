/*
*   Main.c
*   Created by Isabella Stephens on 19/08/2014.
*
*   For the ATMega328P
*/

#define F_CPU 16000000UL     // 16 MHz

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "Shift.h"
//#include "USB.h"
#include "usbdrv/usbdrv.h"
#include "HallEffect.h"

#define LED_REG PORTD
#define LED_DIR DDRD
#define LED     0
#define MODE    1
#define toggleLED() PORTD ^= (1<<LED)

void ledInit(void);
void modeInit(void);

volatile uint8_t on = 0;


int
main(void)
{
    // ISRs are located in NWWR memory
    MCUCR |= (1 << IVCE);
    MCUCR = 0x02;
    
    shiftInit();
    ledInit();
    
    hallEffectInit();
    modeInit();
    cli();
    usbInit();

    _delay_ms(200);
    /*
    shiftDataIn(255);
    shiftDataIn(255);
    shiftToggleLatch();
    shiftToggleFetsLatch();
    */
    sei();
    
    while (1) {
        usbPoll();
    } // Loop indefinitely
}


// Toggle the LED during each interrupt
ISR(INT1_vect)
{
    toggleLED();
    on ^= 1;
    if (on) {
        shiftDataIn(0);
        shiftDataIn(0);
        shiftToggleLatch();
        shiftToggleFetsLatch();
    } else {
        shiftDataIn(255);
        shiftDataIn(255);
        shiftToggleLatch();
        shiftToggleFetsLatch();
    }
}





void
ledInit(void)
{
    // Set the LED as an output and turn it off.
    LED_DIR |= (1 << LED);
    //LED_REG &= ~(1 << LED);
    LED_REG |= (1 << LED);
}


void
modeInit(void)
{
    LED_DIR &= ~(1 << MODE);
}



