
#ifndef DISPLAY_H
#define DISPLAY_H

#include "globalDefs.h"

#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h> // Do we need this??

#include "hallEffect.h"
#include "flash.h"
#include "shift.h"

extern volatile uint8_t mode;

void enable_display(void);
void disable_display(void);
uint8_t display_on(void);

#endif