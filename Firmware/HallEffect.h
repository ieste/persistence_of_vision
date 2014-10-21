

#ifndef HALLEFFECT_H
#define HALLEFFECT_H

#include <avr/io.h>
#include <avr/interrupt.h>

#include "globalDefs.h"

/* Set up the ports/pin for the hall effect switch. */
#define HALL_REG PORTD
#define HALL_DIR DDRD
#define HALL     3

/* The circumference of the wheel in metres (for calculating distance). */
#define CIRCUMFERENCE 1

/**
 * Initialise the hall effect switch by setting it as an input and setting
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
 *
 */
uint32_t get_cycles(void);

/**
 * Get the distance travelled since the board was powered on.
 * Returns: distance travelled (in metres).
 */
uint16_t get_distance(void);

#endif
