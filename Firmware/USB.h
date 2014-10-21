

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