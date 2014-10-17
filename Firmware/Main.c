/*
*   Main.c
*   Created by Isabella Stephens on 19/08/2014.
*
*   For the ATMega328P
*/


#include "Main.h"

volatile uint8_t mode = 0;

int
main(void)
{
    
    initialise();
    
    while (1) {
        usbPoll();
        
        // Manage speed and enable/disable display accordingly.
        if (getSpeed() > 58) {
            enableDisplay();
        } else {}
        
        
    } // Loop indefinitely
}


void initialise(void) {
    // ISRs are located in NRWW memory
    MCUCR |= (1 << IVCE);
    MCUCR = 0x02;
    
    shiftInit();
    ledInit();
    hallEffectInit();
    modeInit();
    cli();
    usbInit();
    //_delay_ms(200);
    sei();
    
    // Set mode
    if (MODE_REG & (1 << MODE)) {
        mode = 1;
        hallEffectDisable();
        setSpeed(200);
    }
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
    MODE_DIR &= ~(1 << MODE);
    
    PCICR |= (1 << PCIE2);
    PCMSK2 |= (1 << PCINT17);
}

ISR(PCINT2_vect) {
    //toggleLED();
    //_delay_ms(1000);
    //LEDoff();
    
    // DEBOUNCE
    // IF MODE = 1, MODE = 2
    // IF MODE = 2, MODE = 3
    // IF MODE = 0, MODE = 4
    // IF MODE = 3, MODE = 0
        // set speed 0
        // hall effect enable
    // IF MODE = 4, MODE = 0
}



