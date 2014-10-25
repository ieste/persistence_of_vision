

#include "hallEffect.h"

/**
 * Flag which stores whether or not the hall effect sensor should be in use.
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
 * Number of timer overflows in the current revolution. Used to calculate clock
 * cycles stored in the cycles variable.
 */
volatile uint32_t overflows = 0;

/**
 * The delay necessary so that if the display is updated every [delay] clock 
 * cycles, the image will be displayed accurately. Calculated by dividing
 * number of cycles in the last revolution by the number of "columns" that need
 * to be displayed in one revolution.
 */
volatile uint16_t delay = 833;


void hall_effect_init(void) {
    
    // Set Hall Effect as an input.
    HALL_DIR &= ~(1 << HALL);
    
    // Disable global interrupts
    cli();
    
    // Interrupt 1 triggers on falling edge (hall effect is active low).
    EICRA = ((EICRA & ~(1 << ISC10)) | (1 << ISC11));
    
    // Enable hall effect interrupt.
    EIMSK |= (1 << INT1);
    
    // Divide clock by 1024 on timer 0.
    TCCR0B |= (1 << CS02) | (1 << CS00);
    
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
    OCR1A = 255;
    TIMSK0 |= (1 << OCIE0A);
    
    // Set the enabled flag and reset the overflow counter and cycles.
    enabled = 1;
    overflows = 0;
    cycles = 0;
    
    sei();
}


void hall_effect_disable(void) {
    
    cli();
    
    // Disable timer overflow interrupt.
    TIMSK0 &= ~(1 << OCIE0A);
    
    // Clear the enabled flag, set cycles to zero and hard code delay rather
    // than having it calculated on the fly.
    enabled = 0;
    cycles = 0;
    delay = 833;
    
    sei();
}


uint32_t get_cycles(void) {
    // If the wheel is going slower than a certain speed, return zero to
    // indicate it is effectively stopped. We also return 0 if overflows
    // exceeds 62, indicating that the wheel has slowed below 60 RPM but not
    // yet made a full revolution (and therefore cycles has not been updated).
    if (!enabled || overflows > 62) {
        return 0;
    } else {
        return cycles;
    }
}


uint32_t get_distance(void) {
    return (revolutions * CIRCUMFERENCE) / 1000;
}


uint16_t get_speed(void) {
    return (uint16_t)(28160000/(cycles/100));
}


/**
 * Count up the number of overflows every time timer0 overflows, allowing us to
 * approximate the number of cycles each revolution.
 */
ISR(TIMER0_COMPA_vect) {
    overflows++;
}

/**
 * Interrupt service routing for handling a pulse from the hall effect 
 * indicating a revolution has been completed.
 */
ISR(INT1_vect)
{
    /**
     * Debounce the hall effect switch by ignoring an interrupt that occurs
     * withing approximately 213 ms of the previous one, indicating the wheel
     * is either traveling faster than 250 RPM (out of spec) or the hall effect
     * has been triggered incorrectly.
     */
    if (overflows < 13) {
        return;
    }
    
    // Only update delay and cycles if the hall effect is enabled.
    if (enabled) {
        
        // Calculate delay based on overflow counter and set current delay.
        if (revolutions > 0) {
            
            // Update cycles.
            cycles = ((uint32_t)overflows * (uint32_t)256 + (uint32_t)TCNT0) *
                    (uint32_t)1024;
            
            // Calculate the delay between pulses for the next revolution.
            delay = cycles/5760;
            // Assuming a max speed of 250 RPM, delay should never be below 666
            if (delay < 666) {
                delay = 666;
            }

            // Reset the clock and overflow counter.
            TCNT0 = 0;
            overflows = 0;
            
            // Tell the display a new revolution has begun.
            start_revolution();
        
        } else {
            // If revolutions is equal to zero, a single revolution has been
            // completed, so we begin timing revolutions.
            hall_effect_enable();
        }
    }
    
    // Increment the number of revolutions for distance calculation.
    revolutions++;
}
