

#include "display.h"


/**
 * Access the mode variable from main so that we know what we should be
 * displaying.
 */
extern volatile uint8_t mode;

/**
 * Our position in the rotation - used to find which address to use when 
 * reading from program memory.
 */
volatile uint16_t position = 0;

/**
 *
 */
volatile uint8_t mosfet = 0;

/**
 * Flag which stores whether or not the display is turned on.
 */
volatile uint8_t on = 0;


extern volatile uint16_t delay;


void enable_display(void) {

    cli();
    TCCR1B |= (1 << CS10); // Divide clock by 1
    
    //TCCR1B |= (1 << CS10) | (1 << CS12); // Divide by 1024
    //OCR1A = 15624; // One second delay (when dividing by 1024).
    OCR1A = delay;
    
    TCCR1B |= (1 << WGM12); // Put timer into CTC mode
    TIMSK1 |= (1 << OCIE1A); // Enable the interrupt
    
    reset_fets();
    position = 0;
    mosfet = 0;
    
    on = 1;

    sei();
}


void disable_display(void) {
    TIMSK1 &= ~(1 << OCIE1A);
    shift_clear();
    on = 0;
}


uint8_t display_on(void) {
    return on;
}


void start_revolution(void) {
    reset_fets();
    position = 0;
    mosfet = 0;
    OCR1A = delay;
}

/**
 * Interrupt service routine for LED driving. Although this would be neater
 * using functions from shift.c, it has instead been hard coded to avoid 
 * function calls so the the number of clock cycles this routine takes is
 * minimised.
 */
ISR(TIMER1_COMPA_vect) {
    
    uint8_t data[2];
    uint8_t i;
    
    // Set output data based on current mode.
    if (mode == 0 || mode == 1) {
        data[0] = read_byte(position);
        data[1] = read_byte(position + 1);
    } else if (mode == 2) {
        data[0] = 255;
        data[1] = 255;
    } else if (mode == 3) {
        data[0] = (mosfet << 7);
        data[1] = 0;
        //data[0] = mosfet*255;
        //data[1] = mosfet*255;
    } else {
        // modify later to deal with mode 4.
        data[0] = 0;
        data[1] = 0;
    }
    
    
    // Output data
    for (i = 0; i < 8; i++) {
        if (data[0] & 128) {
            SHIFT_REG |= (1 << DATA);
        } else {
            SHIFT_REG &= (~(1 << DATA));
        }

        data[0] <<= 1;

        SHIFT_REG ^= (1 << CLOCK);
        SHIFT_REG ^= (1 << CLOCK);
    }
    
    for (i = 0; i < 8; i++) {
        if (data[1] & 128) {
            SHIFT_REG |= (1 << DATA);
        } else {
            SHIFT_REG &= (~(1 << DATA));
        }
        data[1] <<= 1;
        
        SHIFT_REG ^= (1 << CLOCK);
        SHIFT_REG ^= (1 << CLOCK);
    }
    
    toggle_latch_fets();
    toggle_latch();
    
    
    mosfet ^= 1;

    // Increase position. Position wraps around to 0.
    position += 2;
    if (position == 11520) position = 0;
    
    
}