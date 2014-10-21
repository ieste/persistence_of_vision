

#ifndef MAIN_H
#define MAIN_H

#include "globalDefs.h"

#include <avr/io.h>
#include <avr/interrupt.h>

#include "shift.h"
#include "USB.h"
#include "hallEffect.h"
#include "display.h"

/* Set up ports/pin for the mode switch. */
#define MODE_REG    PIND
#define MODE_DIR    DDRD
#define MODE        1

/**
 * Initialise by calling the respective init functions for each of the system
 * components, set registers to indicate interrupts are in NRWW memory, and
 * set the mode.
 */
void initialise(void);

/**
 * Initialise the indicator LED by setting the data direction register to
 * output and turning the LED on.
 */
void LED_init(void);

/**
 * Initialise the mode switch by setting the data direction register, reading
 * in the current mode and setting up pin change interrupts for when the switch
 * is changed.
 */
void mode_init(void);




#endif