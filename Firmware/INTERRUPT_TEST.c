/*
*   INTERRUPT_TEST.c
*   Created by Isabella Stephens on 17/08/2014.
*   Adapted from tutorial at
*    hackaday.com/2010/11/05/avr-programming-03-reading-and-compiling-code/
*
*   For the ATMega328P
*
*   Turns on an LED connected to PD0 in response to an interrupt.
*
*/

#include <avr/io.h>
#include <avr/interrupt.h>


int main(void)
{

    cli();                                  // disable global interrupts
    EICRA |= (1 << ISC01) | (1 << ISC00);   // Interrupts occur on rising edge
    EIMSK |= (1 << INT0);                   // Enable the interrupt
    sei();                                  // enable global interrupts
    
    DDRD |= (1 << 0);                   // Set PD0 to output
    DDRD &= 0b11111011;                 // Set INT0 to input - INT0 is on PD2
    PORTD |= (1 << 0);                  // Set PortD Pin0 high
    
    while (1) {}                        // Loop indefinitely
}


// Toggle the LED during each interrupt (on external interrupt request 0)
ISR(INT0_vect)
{
    PORTD ^= (1<<0);                // Use xor to toggle the LED
}




// General Method of setting an interrupt service routine
//ISR({Vector Source}_vect)
//{
//  ISR code to execute here
//}

// data shared between the ISR an the main program must be volatile and global
// should also make the fetching of this variable atomic in the main execution
// of the program. Use:
//      #include <util/atomic.h>
//      ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
//      {
//          MyValue_Local = MyValue;
//      }









