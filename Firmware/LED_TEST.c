/*
*   LED_TEST.c
*   Created by Isabella Stephens on 15/08/2014.
*   Adapted from tutorial at
*    hackaday.com/2010/11/05/avr-programming-03-reading-and-compiling-code/
*
*   ATMega328P
*
*   Blinks an LED connected to PD0 in response to an interrupt.
*
*/

#include <avr/io.h>
#include <avr/interrupt.h>


int main(void)
{
    
    // Setup the clock and prepare an interrupt every 1 second

    // disable global interrupts
    cli();

    // divide by 64 - Set up the prescaler
    // TCCR1B -> Timer/Counter1 Control Register B
    // To divide by 64 we want to set CS10 and CS11 to 1 on the TCCR1B reg
    // Use the OR operator and left shift a 1 to the location of CS10/11
    TCCR1B |= 1<<CS11 | 1<<CS10;

    // Set target value for clear timer on compare match trigger.
    // count 15624 cycles for 1 second interrupt (last cycle switches the LED)
    OCR1A = 15624;
    
    
    TCCR1B |= 1<<WGM12;             // put timer/counter1 in CTC mode
    
    TIMSK1 |= 1<<OCIE1A;            // enable timer compare interrupt
    
    sei();                          // enable global interrupts
    
    // Set up the I/O for the LED -
    DDRD |= (1 << 0);               // Set data direction register for port D
    PORTD |= (1 << 0);              // Set PortD Pin0 hight
    
    while (1) {}                    // Loop indefinitely
}


// Toggle the LED during each interrupt
// Interrupt service routine for timer/counter1 compare A match
ISR(TIMER1_COMPA_vect)
{
    PORTD ^= (1<<0);                // Use xor to toggle the LED
}



