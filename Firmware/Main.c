

#include "main.h"
#include <avr/sleep.h>
#include "shift.h"


/**
 * Store the mode the board is currently in. 0 = normal operating mode,
 * 1 = test mode 1, 2 = test mode 2, 3 = test mode 3, 4 = distance/speed
 * display mode.
 */
volatile uint8_t mode = 0;


/**
 * Firmware's main control loop which initialises the program and then monitors
 * speed and the USB connection and enables/disables the display accordingly.
 */
int main(void) {
    
    initialise();

    // Loop indefinitely
    while (1) {
        
        // Poll the USB connection.
        //usbPoll();
        /*
        // Manage speed and enable/disable display accordingly.
        if (mode == 0 || mode == 4) {
            if (get_cycles() > 16000000 || get_cycles() == 0) {
                if (display_on()) { // change to if display is on
                    disable_display();
                }
            } else if (~display_on()) { // Change to if display is off
                enable_display();
            }
        }
         */
        
        
    }
}


void initialise(void) {
    
    // ISRs are located in NRWW memory
    MCUCR |= (1 << IVCE);
    MCUCR = 0x02;
    
    // Initialise the system components.
    shift_init();
    LED_init();
    hall_effect_init();
    USB_init();
    mode_init();
    
    // If the mode is 1, we hard code the speed rather than reading from the
    // hall effect switch.
    //if (mode == 1) {
    //    hall_effect_disable();
    //    enable_display();
    //}
    
    // Sleep mode test
    //shift_disable();
    //fets_low();
    //PCICR &= ~(1 << PCIE2);
    //hall_effect_disable();
    //disable_display();
    //sleep_enable();
    //sei();
    //sleep_cpu();
    //sleep_disable();
    //toggleLED();
    //shift_data_in(255);
    toggle_latch();
    toggle_latch();
    
}


void LED_init(void) {
    
    // Set the LED as an output and turn it on.
    LED_DIR |= (1 << LED);
    LEDon();
}


void mode_init(void) {
    
    // Set the mode switch to an input.
    MODE_DIR &= ~(1 << MODE);
    
    // Read in the current mode.
    if (MODE_REG & (1 << MODE)) {
        mode = 1;
    } else {
        mode = 0;
    }
    
    // Enable pin change interrupts on the mode switch.
    PCMSK2 |= (1 << PCINT17);
    PCICR |= (1 << PCIE2);
}


/**
 * ISR to respond to the mode switch being changed. Will update the mode
 * variable and make any necessary changes to the display/hall effect
 * interrupts.
 */
ISR(PCINT2_vect) {
    
    //toggleLED();
    
    if (mode == 0) {
        mode = 4;
    } else if (mode == 4) {
        mode = 0;
    } else if (mode == 1) {
        mode = 2;
    } else if (mode == 2) {
        mode = 3;
    } else if (mode == 3) {
        mode = 0;
        hall_effect_enable();
    }
}



