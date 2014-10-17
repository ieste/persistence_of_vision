


#ifndef HALLEFFECT_H
#define HALLEFFECT_H

#include <avr/io.h>
#include <avr/interrupt.h>


#define HALL_REG PORTD
#define HALL_DIR DDRD

#define HALL     3

void hallEffectInit(void);
void hallEffectDisable(void);
void hallEffectEnable(void);

uint8_t getSpeed(void);
void setSpeed(uint8_t s);


#endif
