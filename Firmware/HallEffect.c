

#include "hallEffect.h"

/**
 *
 */
volatile uint8_t enabled = 0;

/**
 * The number of clock cycles elapsed during the previous revolution.
 */
volatile uint32_t cycles = 0;

/**
 * The number of revolutions the wheel has made. Used for calculating distance
 * travelled. May be prone to inaccuracies if frequently waking from sleep. As
 * this can cause the interrupt to not trigger.
 */
volatile uint32_t revolutions = 0;

/**
 *
 */
volatile uint32_t overflows = 0;


volatile uint16_t delay = 833;


void hall_effect_init(void) {
    
    // Set Hall Effect as input
    HALL_DIR &= ~(1 << HALL);
    
    // Disable global interrupts
    cli();
    
    // Interrupt 1 triggers on falling edge (hall effect is active low).
    EICRA = ((EICRA & ~(1 << ISC10)) | (1 << ISC11));
    
    // Enable hall effect interrupt.
    EIMSK |= (1 << INT1);
    
    // Divide clock by 64 on timer 0.
    //TCCR0B |= (1 << CS01) | (1 << CS00);
    // Divide clock by 1 on timer 0.
    //TCCR0B |= (1 << CS00);
    // Divide clock by 1024 on timer 0.
    TCCR0B |= (1 << CS02) | (1 << CS00);
    OCR1A = 255;
    
    // Set flag to enable the timer interrupts for the hall effect (they are
    // actually enabled once one revolution has been completed).
    enabled = 1;
    
    // Enable global interrupts
    sei();
}


void hall_effect_enable(void) {
    
    cli();
    
    // Set the timer to zero and enable the timer overflow interrupt.
    TCNT0 = 0;
    //TIMSK0 |= (1 << TOIE0);
    TIMSK0 |= (1 << OCIE0A);
    
    // Set the enabled flag and reset the overflow counter.
    enabled = 1;
    overflows = 0;
    cycles = 0;
    
    sei();
}


void hall_effect_disable(void) {
    
    cli();
    
    // Disable timer overflow interrupt.
    TIMSK0 &= ~(1 << TOIE0);
    
    // Clear the enabled flag, set cycles to zero and hard code delay.
    enabled = 0;
    cycles = 0;
    delay = 833;
    
    sei();
}


uint32_t get_cycles(void) {
    // If the wheel is going slower than a certain speed, return zero to
    // indicate it is effectively stopped.
    if (!enabled || overflows > 65) {
        return 0;
    } else {
        return cycles;
    }
}


uint32_t get_distance(void) {
    return revolutions * CIRCUMFERENCE;
}


//ISR(TIMER0_OVF_vect) {
ISR(TIMER0_COMPA_vect) {
    overflows++;
}


ISR(INT1_vect)
{
    if (overflows < 13) {
        //if (TIFR0 & (1 << TOV0)) toggleLED();
        if (TIFR0 & (1 << OCF0A)) toggleLED();
        return;
    }
    
    //toggleLED();
    
    if (enabled) {
        // Calculate delay based on overflow counter and set current delay.
        if (revolutions > 0) {
            
            cycles = ((uint32_t)overflows * (uint32_t)256 + (uint32_t)TCNT0) *
                    (uint32_t)1024;
            
            // Calculate the delay between pulses for the next revolution.
            delay = cycles/5760;
            if (delay < 666) {
                delay = 666;
            }

            // Reset the clock and overflow counter.
            TCNT0 = 0;
            overflows = 0;
            
            // Set the delay and reset the position to begin a new revolution.
            start_revolution();
            
        } else {
            // A single revolution has been completed, so we begin timing
            // revolutions.
            hall_effect_enable();
        }
    }
    
    // Increment the number of revolutions for distance calculation.
    revolutions++;
}
