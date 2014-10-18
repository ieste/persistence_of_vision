
#ifndef MAIN_H
#define MAIN_H


#define F_CPU 16000000UL     // 16 MHz

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "shift.h"
//#include "USB.h"
#include "usbdrv/usbdrv.h"
#include "hallEffect.h"
#include "display.h"

#define LED_REG PORTD
#define LED_DIR DDRD
#define MODE_REG PIND
#define MODE_DIR PORTD
#define LED     0
#define MODE    1
#define toggleLED() PORTD ^= (1<<LED)
#define LEDon() PORTD |= (1 << LED)
#define LEDoff() PORTD &= ~(1 << LED)

void LED_init(void);
void mode_init(void);
void initialise(void);



#endif