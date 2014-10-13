
#ifndef SHIFT_H
#define SHIFT_H

#include <avr/io.h>

#define LATCH   3     // Green
#define CLOCK   4     // Yellow
#define DATA    5      // Blue
#define FET2    2      // White
#define FET1    1      // White
#define ENABLE  0

#define SHIFT_REG PORTC
#define SHIFT_DIR DDRC

void shiftDataIn(uint8_t data);
void shiftInit(void);
void shiftToggleLatch(void);
void shiftToggleFetsLatch(void);

#endif