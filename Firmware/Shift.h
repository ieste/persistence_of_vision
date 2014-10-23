
#ifndef SHIFT_H
#define SHIFT_H

#include <avr/io.h>

/* Name the IO pins for the shift registers. */
#define LATCH   3
#define CLOCK   4
#define DATA    5
#define FET1    1
#define FET2    2
#define ENABLE  0

/* Name the ports for the shift registers. */
#define SHIFT_REG PORTC
#define SHIFT_DIR DDRC

/* Define macros to toggle the latch and MOSFETs. */
#define toggle_latch() SHIFT_REG ^= (1 << LATCH)
#define toggle_latch_fets() SHIFT_REG ^= (1 << FET1) | (1 << FET2) | (1 << LATCH)

/**
 * Macro to reset the state of the fets so that FET1 is on and FET2 is off.
 * This is important to ensure that the data does not get flipped when a new
 * revolution starts.
 */
#define reset_fets() SHIFT_REG = (SHIFT_REG & ~(1 << FET2)) | (1 << FET1)
#define fets_low()   SHIFT_REG &= ~((1 << FET1) | (1 << FET2))
#define fets_high()  SHIFT_REG |= ((1 << FET1) | (1 << FET2))

/**
 * Initialise the shift registers by setting the data direction registers
 * and setting initial values on the ports. All LEDs are turned off the begin
 * with.
 */
void shift_init(void);

/**
 * Shift 8 bits of data in to the shift register.
 * Params: the data we are shifting in - MSB is shifted in first.
 * (Note: this function does not perform latching (i.e. data is not 
 * automatically output to the LEDs).
 */
void shift_data_in(uint8_t data);

/**
 * Shift 16 bits (2 bytes) of data in to the shift register and latch.
 * Params: the data we are shifting in (an array of two bytes). The MSB of the
 * first byte in data is shifted in first.
 */
void output_data(uint8_t* data);

/**
 * Clear the shift registers by shifting in zeros and then latching. This 
 * method does not toggle the mosfets.
 */
void shift_clear(void);


#endif