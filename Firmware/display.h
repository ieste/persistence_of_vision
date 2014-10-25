
/**
 * The display.h and display.c files contain high level functionality for
 * controlling the LED display (somewhat abstracted from the functioning of the
 * shift registers.
 *
 * All of the methods in this library have been placed in the RWW section of
 * program memory. This is because of memory restrictions in the NRWW section
 * of memory where the majority of the program is located.
 */

#ifndef DISPLAY_H
#define DISPLAY_H

#include "globalDefs.h"

#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>

#include "hallEffect.h"
#include "flash.h"
#include "shift.h"

/**
 * Turn on the display by setting up and enabling the necessary interrupt, and
 * setting other relevant flags with the start_revolution method.
 */
void RWW_SECTION enable_display(void);

/**
 * Turn the display off by disabling interrupts that update the display, and
 * clearing the display contents.
 */
void RWW_SECTION disable_display(void);

/**
 * Get the status of the display.
 * Returns: 1 if the display is off, 0 if it is on.
 */
uint8_t RWW_SECTION display_on(void);

/**
 * Do the set-up for a new revolution - reset the timer, update the delay, 
 * reset the position and reset the state of the MOSFETs.
 */
void RWW_SECTION start_revolution(void);

/**
 * Get data (1 byte) to shift in to the shift registers in order to display
 * the speed in metres/second at the top of the wheel.
 * Returns: 1 byte of display data so that the speed is displayed.
 */
uint8_t RWW_SECTION get_speed_display_data(void);

/**
 * Get data (1 byte) to shift in to the shift registers in order to display
 * the distance in metres at the top of the wheel.
 * Returns: 1 byte of display data so that the distance is displayed.
 */
uint8_t RWW_SECTION get_distance_display_data(void);

#endif