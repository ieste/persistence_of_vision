

#ifndef GLOBALDEFS_H
#define GLOBALDEFS_H

#define F_CPU 16000000UL     // 16 MHz

#define LED_REG PORTD
#define LED_DIR DDRD

#define LED     0

#define toggleLED() PORTD ^= (1<<LED)
#define LEDon() PORTD |= (1 << LED)
#define LEDoff() PORTD &= ~(1 << LED)




#endif
