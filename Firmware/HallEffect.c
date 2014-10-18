

#include "hallEffect.h"
#include "main.h" //REMOVE LATER

volatile uint8_t enabled = 0;

volatile uint8_t speed = 0;

volatile uint32_t revolutions = 0;

volatile uint32_t overflows = 0;


void hall_effect_init(void) {
    
    // Set Hall Effect as input
    HALL_DIR &= ~(1 << HALL);
    
    // Disable global interrupts
    cli();
    
    // Interrupt 1 triggers on falling edge (hall effect is active low).
    EICRA = ((EICRA & ~(1 << ISC10)) | (1 << ISC11));
    
    // Divide clock by 64 on timer 0.
    TCCR0B |= (1 << CS01) | (1 << CS00);
    
    // Enable the interrupts for the hall effect.
    hall_effect_enable();
    
    // Enable global interrupts
    sei();
}


void hall_effect_disable(void) {
    
    // Disable timer overflow interrupt.
    TIMSK0 &= ~(1 << TOIE0);
    
    // Clear the enabled flag.
    enabled = 0;
}


void hall_effect_enable(void) {
    
    // Enable hall effect interrupt.
    EIMSK |= (1 << INT1);
    
    // Enable timer overflow interrupt.
    TIMSK0 |= (1 << TOIE0);
    
    // Set the enabled flag and reset the overflow counter.
    enabled = 1;
    overflows = 0;
}


uint8_t get_speed(void) {
    
    // If no revolution has been sensed in five seconds set the speed to 0.
    if (overflows > 5000) {
        set_speed(0);
    }
    
    return speed;
}


void set_speed(uint8_t s) {
    speed = s;
}


uint16_t get_distance(void) {
    return revolutions * CIRCUMFERENCE;
}


ISR(TIMER0_OVF_vect) {
    overflows++;
}


ISR(INT1_vect)
{
    // Increment the number of revolutions for distance calculation.
    revolutions++;
    
    // Calculate speed based on overflow counter and set current speed.
    if (enabled) {
        
        speed = 60;
        
        // Reset the overflow counter.
        overflows = 0;
    }
}


