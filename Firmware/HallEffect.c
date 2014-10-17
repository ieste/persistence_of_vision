

#include "HallEffect.h"


volatile uint32_t ovf = 0;
volatile uint8_t ison = 0;
volatile uint8_t speed = 0;


void hallEffectInit(void) {
    
    // Set Hall Effect as input
    HALL_DIR &= ~(1 << HALL);
    
    // Disable global interrupts
    cli();
    
    // Interrupt 1 triggers on falling edge (hall effect is active low)
    EICRA = ((EICRA & ~(1 << ISC10)) | (1 << ISC11));
    
    // Divide clock by 64 on timer 0
    TCCR0B |= (1 << CS01) | (1 << CS00);
    
    // Enable the interrupts for the hall effect
    hallEffectEnable();
    
    // Enable global interrupts
    sei();
}


void hallEffectDisable(void) {
    // Disable hall effect interrupt.
    EIMSK &= ~(1 << INT1);
    // Disable timer overflow interrupt.
    TIMSK0 &= ~(1 << TOIE0);
}


void hallEffectEnable(void) {
    // Enable hall effect interrupt.
    EIMSK |= (1 << INT1);
    // Enable timer overflow interrupt.
    TIMSK0 |= (1 << TOIE0);
}


uint8_t getSpeed(void) {
    if (ovf > 5000) setSpeed(0);
    return speed;
}


void setSpeed(uint8_t s) {
    speed = s;
}


ISR(TIMER0_OVF_vect) {
    ovf++;
}


// Toggle the LED during each interrupt
ISR(INT1_vect)
{
    
    // Calculate speed based on overflow counter and current speed.
    
    
    // Reset the overflow counter.
    ovf = 0;
    
    /*
    
    if (ovf > 255) {
        LEDoff();
    } else {
        LEDon();
    }
    //toggleLED();
    ison ^= 1;
    if (ison) {
        shiftDataIn(0);
        shiftDataIn(0);
        shiftToggleLatch();
        shiftToggleFetsLatch();
    } else {
        shiftDataIn(255);
        shiftDataIn(255);
        shiftToggleLatch();
        shiftToggleFetsLatch();
    }
    */
}


