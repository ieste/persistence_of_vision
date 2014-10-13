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

#define LED 0
#define HALL 3


int main(void)
{

    cli();                                  // disable global interrupts

    // Interrupt 1 triggers on falling edge.
    EICRA = ((EICRA & ~(1 << ISC10)) | (1 << ISC11));
    
    EIMSK |= (1 << INT1);                   // Enable the interrupt
    sei();                                  // enable global interrupts
    
    DDRD |= (1 << LED);                     // Set PD0 (LED) to output
    DDRD &= ~HALL;                          // Set PD3 (INT1) to input
    PORTD |= (1 << LED);                    // Set LED high
    
    while (1) {}                            // Loop indefinitely
}


// Toggle the LED during each interrupt
ISR(INT1_vect)
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









