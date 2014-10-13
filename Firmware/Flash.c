

#include "Flash.h"

void read_page(uint16_t pageAddress, uint8_t* buffer) {
    
    uint8_t i;
    uint32_t page = PAGESIZE * pageAddress;

    for (i = 0; i < PAGESIZE; i++) {
        *buffer++ = pgm_read_byte_near(page + i);
    }
}


void write_page(uint16_t pageAddress, uint8_t* buffer) {

    uint8_t i;
    uint32_t page = PAGESIZE * pageAddress;
    
    boot_page_erase_safe(page);
    
    boot_spm_busy_wait();
    
    for (i = 0; i < PAGESIZE; i+=2) {
        uint16_t word = *buffer++;
        word += (*buffer++) << 8;
        cli();
        boot_page_fill(page + i, word);
        sei();
    }
    
    boot_page_write_safe(page);
    
    boot_rww_enable_safe();
}