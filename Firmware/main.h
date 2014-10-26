
/**
 * The main.h and main.c files contain the main control loop of the program, 
 * and handle high level operations such as initialising the hardware, managing
 * the mode of the software and
 */

#ifndef MAIN_H
#define MAIN_H

#include "globalDefs.h"

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <util/delay.h>

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

/**
 * Puts the AVR in to sleep mode in order to reduce power consumption.
 */
void sleep(void);




#endif