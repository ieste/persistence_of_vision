
#ifndef DISPLAY_H
#define DISPLAY_H

#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>

#include "main.h" // needed to get mode??
#include "hallEffect.h"
#include "flash.h"
#include "shift.h" // Merge??

extern volatile uint8_t mode;

void enableDisplay(void);
void disableDisplay(void);

#endif