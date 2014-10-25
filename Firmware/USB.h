/**
 * The USB.h and USB.c files are an extension of the V-USB library available at
 * http://www.obdev.at/products/vusb/index.html. It provides functionality
 * for sending and receiving data via USB without the use of an external chip
 * such as an FTDI chip.
 *
 * The majority of this code is documented in the usbdrv.h file available in 
 * the usbdrv folder. 
 */

#ifndef USB_H
#define USB_H

#include "globalDefs.h"

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#include "usbdrv/usbdrv.h"

#include "flash.h"

/**
 * Initialise USB communication by calling the driver's initialise function.
 */
void USB_init(void);

/* Other methods documented in usbdrv/usbdrv.h. */

#endif