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
#include <util/delay.h>

#define LATCH 2     // Green
#define CLOCK 4     // Yellow
#define DATA 5      // Blue
#define SHIFT_REG PORTC
#define SHIFT_DIR DDRC



int
main(void)
{
    // Set the Latch, Clock and Data lines as outputs.
    SHIFT_DIR |= (1 << LATCH) | (1 << CLOCK) | (1 << DATA);
    // Set the Latch, Clock and Data lines low.
    SHIFT_REG &= ~((1 << LATCH) | (1 << CLOCK) | (1 << DATA));
    
    while (1) { // Loop indefinitely
        toggle_latch();
        shift_data_in(0b10101010);
        _delay_ms(2000);
        toggle_latch();
        shift_data_in(0b01010101);
        _delay_ms(2000);
    }
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
shift_data_in (char data)
{
    char i = 0;
    
    for (i = 7; i >= 0; i--)
    {
        if ((data >> i) & 1)
            SHIFT_REG |= (1 << DATA);
        else
            SHIFT_REG &= (~(1 << DATA));
        
        SHIFT_REG ^= (1 << CLOCK);
        _delay_us(1);
        SHIFT_REG ^= (1 << CLOCK);
    }
    
    SHIFT_REG &= (~(1 << LATCH));
}

