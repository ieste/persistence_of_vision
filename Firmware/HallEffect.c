

#include "HallEffect.h"

void hallEffectInit(void) {
    
    // Set Hall Effect as input
    HALL_DIR &= ~(1 << HALL);
    
    // disable global interrupts
    cli();
    // Interrupt 1 triggers on falling edge.
    EICRA = ((EICRA & ~(1 << ISC10)) | (1 << ISC11));
    // Enable the interrupt
    EIMSK |= (1 << INT1);
    // Enable global interrupts
    sei();
}