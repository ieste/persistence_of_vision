

#include "hallEffect.h"

/**
 *
 */
volatile uint8_t enabled = 0;

/**
 *
 */
volatile uint32_t cycles = 0;

/**
 *
 */
volatile uint32_t revolutions = 0;

/**
 *
 */
volatile uint32_t overflows = 0;


void hall_effect_init(void) {
    
    // Set Hall Effect as input
    HALL_DIR &= ~(1 << HALL);
    
    // Disable global interrupts
    cli();
    
    // Interrupt 1 triggers on falling edge (hall effect is active low).
    EICRA = ((EICRA & ~(1 << ISC10)) | (1 << ISC11));
    
    // Divide clock by 64 on timer 0.
    //TCCR0B |= (1 << CS01) | (1 << CS00);
    // Divide clock by 1 on timer 0.
    TCCR0B |= (1 << CS00);
    
    // Enable hall effect interrupt.
    EIMSK |= (1 << INT1);
    
    // Enable the interrupts for the hall effect.
    //hall_effect_enable();
    enabled = 1;
    
    // Enable global interrupts
    sei();
}


void hall_effect_enable(void) {
    
    // Enable timer overflow interrupt.
    TIMSK0 |= (1 << TOIE0);
    
    // Set the enabled flag and reset the overflow counter.
    enabled = 1;
    overflows = 0;
    cycles = 0;
}


void hall_effect_disable(void) {
    
    // Disable timer overflow interrupt.
    TIMSK0 &= ~(1 << TOIE0);
    
    // Clear the enabled flag.
    enabled = 0;
}


uint32_t get_cycles(void) {
    // If the wheel is going slower that.. ? Return zero to indicate the wheel
    // is effectively stopped.
    if (~enabled || overflows > 125500) {
        return 0;
    } else {
        return cycles;
    }
}


uint16_t get_distance(void) {
    return revolutions * CIRCUMFERENCE;
}


ISR(TIMER0_OVF_vect) {
    overflows++;
}


ISR(INT1_vect)
{
    if (revolutions == 0 && enabled) {
        hall_effect_enable();
    }
    
    // Increment the number of revolutions for distance calculation.
    revolutions++;
    
    // Calculate delay based on overflow counter and set current delay.
    if (enabled) {
        
        cycles = overflows * 255 + TCNT0;
        
        // Reset the overflow counter.
        overflows = 0;
    }
}


