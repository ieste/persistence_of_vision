

#include "shift.h"


void shift_init(void) {
    
    // Set the Latch, Clock and Data, FETs and enable lines as outputs.
    SHIFT_DIR |= (1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << FET1) |
            (1 << FET2) | (1 << ENABLE);
    
    // Set the Latch, Clock, Data and enable lines low. Also MOSFET 2.
    SHIFT_REG &= ~((1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << FET2) |
            (1 << ENABLE));
    
    // Set MOSFET 1 high.
    SHIFT_REG |= (1 << FET1);
    
    // Set all outputs to 0 (LEDs off) to begin with.
    shift_clear();
}


void shift_data_in(uint8_t data) {

    uint8_t i;
    
    // Loop through each bit in the byte and shift it in to the register.
    for (i = 0; i < 8; i++)
    {
        /*
        if ((data >> (7 - i)) & 1) {
            SHIFT_REG |= (1 << DATA);
        } else {
            SHIFT_REG &= (~(1 << DATA));
        }
        */
        
        // More efficient:
        
        if (data & 128) {
            SHIFT_REG |= (1 << DATA);
        } else {
            SHIFT_REG &= (~(1 << DATA));
        }
        
        data <<= 1;
        
        // Pulse the clock
        SHIFT_REG ^= (1 << CLOCK);
        SHIFT_REG ^= (1 << CLOCK);
    }
}


void output_data(uint8_t* data) {
    // Shift in the data.
    shift_data_in(data[0]);
    shift_data_in(data[1]);
    
    // Perform latching and switch the MOSFETs.
    toggle_latch_fets();
    toggle_latch();
}


void shift_clear(void) {
    // Shift in zeros.
    shift_data_in(0);
    shift_data_in(0);
    
    // Perform latching without modifying the state of the MOSFETs.
    toggle_latch();
    toggle_latch();
}


void shift_disable(void) {
    SHIFT_REG &= ~(1 << ENABLE);
}
