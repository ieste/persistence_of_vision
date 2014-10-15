
#ifndef MAIN_H
#define MAIN_H


#define F_CPU 16000000UL     // 16 MHz

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "Shift.h"
//#include "USB.h"
#include "usbdrv/usbdrv.h"
#include "HallEffect.h"

#define LED_REG PORTD
#define LED_DIR DDRD
#define LED     0
#define MODE    1
#define toggleLED() PORTD ^= (1<<LED)
#define LEDon() PORTD |= (1 << LED)
#define LEDoff() PORTD &= ~(1 << LED)

void ledInit(void);
void modeInit(void);




#endif