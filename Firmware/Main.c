

#include "main.h"

volatile uint8_t mode = 0;

int main(void) {
    
    initialise();

    // Loop indefinitely
    while (1) {
        
        usbPoll();
        
        //enableDisplay();
        
        // Manage speed and enable/disable display accordingly.
        /*
        if (get_speed() > 58) {
        //toggleLED();
        //LEDoff();
            enableDisplay();
        } else {
            disableDisplay();
        }
        */
        
    }
}


void initialise(void) {
    
    // ISRs are located in NRWW memory
    MCUCR |= (1 << IVCE);
    MCUCR = 0x02;
    
    shiftInit();
    LED_init();
    hall_effect_init();
    mode_init();
    
    cli();
    usbInit();
    _delay_ms(200);
    sei();
    
    // Set mode
    if (MODE_REG & (1 << MODE)) {
        mode = 1;
        hall_effect_disable();
        set_speed(0);
    }
}

void LED_init(void) {
    // Set the LED as an output and turn it on.
    LED_DIR |= (1 << LED);
    LEDon();
}


void mode_init(void) {
    // Set the mode switch to an input.
    MODE_DIR &= ~(1 << MODE);
    
    // Enable pin change interrupts on the mode switch.
    PCMSK2 |= (1 << PCINT17);
    PCICR |= (1 << PCIE2);
}


ISR(PCINT2_vect) {
    // TODO: Validate with input value (if high, mode should be odd)
    //uint8_t mode_high = MODE_REG & (1 << MODE);
    
    //toggleLED();
    if (mode == 0) {
        mode = 4;
        disableDisplay();
    } else if (mode == 4) {
        mode = 0;
        enableDisplay();
    } else if (mode == 1) {
        mode = 2;
    } else if (mode == 2) {
        mode = 3;
    } else if (mode == 3) {
        mode = 0;
        // Set speed to 0
        // Enable hall effect sensors
        set_speed(0);
        hall_effect_enable();
    }
}



