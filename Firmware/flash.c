

#include "flash.h"


void read_page(uint16_t pageAddress, uint8_t* buffer) {
    
    uint8_t i;
    
    // Convert the page address into a byte address.
    uint32_t page = PAGE_SIZE * pageAddress + ADDRESS_OFFSET;

    // Loop through each byte in the page and place it in the buffer.
    for (i = 0; i < PAGE_SIZE; i++) {
        *buffer++ = pgm_read_byte_near(page + i);
    }
}


void write_page(uint16_t pageAddress, uint8_t* buffer) {

    uint8_t i;
    
    // Convert the page address into a byte address.
    uint32_t page = PAGE_SIZE * pageAddress + ADDRESS_OFFSET;
    
    // Erase the page we are writing to (and wait for this to finish).
    boot_page_erase_safe(page);
    boot_spm_busy_wait();
    
    // Iterate through the buffer, converting every two bytes into a word and
    // filling the page with data.
    for (i = 0; i < PAGE_SIZE; i+=2) {
        uint16_t word = *buffer++;
        word += (*buffer++) << 8;
        cli();
        boot_page_fill(page + i, word);
        sei();
    }
    boot_spm_busy_wait();
    
    // Write the page into program memory.
    cli();
    boot_page_write(page);
    sei();
    boot_spm_busy_wait();
    
    // Enable the RWW section of program memory so we can read from it later.
    boot_rww_enable_safe();
}

/*
uint32_t read_dword(uint16_t byteAddress) {
    return pgm_read_dword(byteAddress);
}
*/

/*
uint16_t read_word(uint16_t byteAddress) {
    return pgm_read_word(byteAddress);
}
*/

uint8_t read_byte(uint16_t byteAddress) {
    return pgm_read_byte(byteAddress);
}