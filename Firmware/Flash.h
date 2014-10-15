

#ifndef FLASH_H
#define FLASH_H

#include <avr/boot.h>
#include <avr/pgmspace.h>
#include <avr/interrupt.h>

#define PAGESIZE SPM_PAGESIZE

void read_page(uint16_t pageAddress, uint8_t* buffer);
void read_dword(uint16_t byteAddress);
void write_page(uint16_t pageAddress, uint8_t* buffer);

#endif