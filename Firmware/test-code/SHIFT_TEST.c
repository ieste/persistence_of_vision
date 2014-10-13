/*
*   SHIFT_TEST.c
*   Created by Isabella Stephens on 19/08/2014.
*
*   For the ATMega328P
*
*   PC5 Blue Serial Data Line
*   PC4 Green ST_CP Latch Line
*   PC3 Yellow SH_CP Clock Line
*   Toggle LEDs attached to a shift register: 74HC595
*/

#define F_CPU 16000000UL     // 16 MHz

#include <avr/io.h>
#include <util/delay.h> // These delay functions do not appear to give
                        // reliable delays. Internal clock used instead.
#include <avr/interrupt.h>

#define LATCH 2     // Green
#define CLOCK 4     // Yellow
#define DATA 5      // Blue
#define SHIFT_REG PORTC
#define SHIFT_DIR DDRC
#define LED 1

void set_up_clock(void);

volatile uint8_t flag;

int
main(void)
{
    // Set the Latch, Clock and Data lines as outputs.
    SHIFT_DIR |= (1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << LED);
    // Set the Latch, Clock and Data lines low.
    SHIFT_REG &= ~((1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << LED));
    
    set_up_clock();
    flag = 0;
    
    
    while (1) {} // Loop indefinitely
}


void
toggle_latch (void)
{
    // Delay for 100 ns to ensure latching succeeds.
    _delay_us(1);
    // Toggle the latch.
    SHIFT_REG ^= (1 << LATCH);
    
    
}

void
shift_data_in (uint8_t data)
{
    
    for (uint8_t i = 0; i < 8; i++)
    {
        if (((data >> (7 - i)) & 1))
            SHIFT_REG |= (1 << DATA);
        else
            SHIFT_REG &= (~(1 << DATA));
        
        SHIFT_REG ^= (1 << CLOCK);
        _delay_us(1);
        SHIFT_REG ^= (1 << CLOCK);
    }
    
    toggle_latch();
}

void
set_up_clock (void)
{
    cli();  // disable interrupts while setting up
    TCCR1B |= (1 << CS12) | (1 << CS10);    // Divide clock by 1024
    OCR1A = 15624;  // 1 second
    TCCR1B |= (1 << WGM12); // Put timer into CTC mode
    TIMSK1 |= (1 << OCIE1A); // Enable the timer compare interrupt
    sei();  // enable interrupts
}

//interrupt service routine for timer
ISR(TIMER1_COMPA_vect)
{
    SHIFT_REG ^= (1 << LED);
    
    if (flag) {
        flag = 0;
        toggle_latch();
        shift_data_in(170);
        
    } else {
        flag = 1;
        toggle_latch();
        shift_data_in(85);
    }
    
    
}

