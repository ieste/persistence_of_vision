/*
*   Main.c
*   Created by Isabella Stephens on 19/08/2014.
*
*   For the ATMega328P
*/


#include "Main.h"



int
main(void)
{
    // ISRs are located in NRWW memory
    MCUCR |= (1 << IVCE);
    MCUCR = 0x02;
    
    shiftInit();
    ledInit();
    
    hallEffectInit();
    modeInit();
    cli();
    usbInit();

    
    _delay_ms(200);
    sei();

    
    while (1) {
        usbPoll();
    } // Loop indefinitely
}




void
ledInit(void)
{
    // Set the LED as an output and turn it on.
    LED_DIR |= (1 << LED);
    //LED_REG &= ~(1 << LED);
    LED_REG |= (1 << LED);
}


void
modeInit(void)
{
    LED_DIR &= ~(1 << MODE);
    PCICR |= (1 << PCIE2);
    PCMSK2 |= (1 << PCINT17);
}

ISR(PCINT17_vect) {
    //toggleLED();
    //_delay_ms(1000);
    //LEDoff();
}



