/**
 * The globalDefs.h file contains definitions used throughout the firmware.
 */

#ifndef GLOBALDEFS_H
#define GLOBALDEFS_H

/* Set CPU speed to 16 MHz. */
#define F_CPU 16000000UL

/**
 * 
 */
#define RWW_SECTION __attribute__ ((section (".rwwsection")))

#define ADDRESS_OFFSET 4096

/**
 * LED macros used by multiple files.
 */
#define LED_REG PORTD
#define LED_DIR DDRD
#define LED     0

#define toggle_LED() PORTD ^= (1<<LED)
#define LED_on()     PORTD |= (1 << LED)
#define LED_off()    PORTD &= ~(1 << LED)


#endif
