/**
 * The flash.h and flash.c files provide functionality for reading from and 
 * writing to the AVR's program memory. These methods need to be place in the 
 * bootloader (NRWW) section of program memory or they will not work.
 */
#ifndef FLASH_H
#define FLASH_H

#include "globalDefs.h"

#include <avr/boot.h>
#include <avr/pgmspace.h>
#include <avr/interrupt.h>

#define PAGE_SIZE SPM_PAGESIZE

/**
 * Reads a page from the AVR's program memory.
 * Params: the address (in pages) of the page we want to read, a buffer we 
 * write the page contents in to.
 */
void read_page(uint16_t pageAddress, uint8_t* buffer);

/**
 * Writes a page into the AVR's program memory.
 * Params: the address (in pages) of the page we want to write to, a buffer 
 * containing the data (128 bytes) we want to write into the page.
 * (Note: this function will only work if it is being called from NRWW memory).
 */
void write_page(uint16_t pageAddress, uint8_t* buffer);

/**
 * Reads a byte from the AVR's program memory.
 * Params: the address (in bytes) of the byte we want to read.
 * Returns: the byte read.
 */
uint8_t read_byte(uint16_t byteAddress);

#endif