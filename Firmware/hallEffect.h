
/**
 * The hallEffect.h and hallEffect.c files contain methods for making use of 
 * the hall effect switch on the board. This includes handling the input from
 * the switch via an interrupt service routine, as well as timing revolutions
 * of the wheel using timer0.
 */

#ifndef HALLEFFECT_H
#define HALLEFFECT_H

#include <avr/io.h>
#include <avr/interrupt.h>

#include "globalDefs.h"
#include "display.h"

/* Set up the ports/pin for the hall effect switch. */
#define HALL_REG PORTD
#define HALL_DIR DDRD
#define HALL     3

/* The circumference of the wheel in mm (for calculating distance). */
#define CIRCUMFERENCE 1760

/**
 * Initialise the hall effect switch by setting it as an input, setting
 * up a timer to count time since the last revolution was completed, and an 
 * interrupt which fires when a revolution has occurred.
 */
void hall_effect_init(void);

/**
 * Enable the timer and interrupt on the hall effect switch.
 */
void hall_effect_enable(void);

/**
 * Disable the timer on the hall effect switch and stop calculating speed.
 */
void hall_effect_disable(void);

/**
 * Retreive the number of clock cycles which occurred during the last full
 * revolution.
 * Returns: approximate number of cycles in last revolution, or 0 if the hall
 * effect is disabled or the number of cycles indicates that the display should
 * be off.
 */
uint32_t get_cycles(void);

/**
 * Get the distance travelled since the board was powered on.
 * Returns: distance travelled (in metres).
 */
uint32_t get_distance(void);

/**
 * Get the speed travelled by the wheel.
 * Returns: speed travelled in m/s.
 */
uint16_t get_speed(void);

#endif
