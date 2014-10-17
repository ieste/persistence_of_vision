

#include "Shift.h"


void shiftInit(void) {
    
    // Set the Latch, Clock and Data, FETs and enable lines as outputs.
    SHIFT_DIR |= (1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << FET1)
                 | (1 << FET2) | (1 << ENABLE);
    
    // Set the Latch, Clock, Data and enable lines low. Also MOSFET 2.
    SHIFT_REG &= ~((1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << FET2)
                 | (1 << ENABLE));
    
    // Set MOSFET 1 high.
    SHIFT_REG |= (1 << FET1);
    
    // Set all outputs to 0 to begin with.
    shiftDataIn(0);
    shiftDataIn(0);
    shiftLatch();
    shiftLatchFets();
}



void
shiftDataIn(uint8_t data)
{
    uint8_t i;
    
    for (i = 0; i < 8; i++)
    {
        if (((data >> (7 - i)) & 1))
            SHIFT_REG |= (1 << DATA);
        else
            SHIFT_REG &= (~(1 << DATA));
        
        // Pulse the clock
        SHIFT_REG ^= (1 << CLOCK);
        SHIFT_REG ^= (1 << CLOCK);
    }
}