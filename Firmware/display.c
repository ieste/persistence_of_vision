
#include "display.h"

#define ACCURACY 6

// Store whether display is on so others can access this information.
extern volatile uint8_t mode;
volatile uint16_t position = 0;
volatile uint8_t mosfet = 0;
volatile uint8_t bitPosition = 0;
volatile uint8_t on = 0;
volatile uint16_t delay = 480;
//volatile uint16_t delay = 6;

volatile uint8_t degree[ACCURACY];

void enable_display(void) {

    cli();
    TCCR1B |= (1 << CS10); // Divide clock by 1
    //TCCR1B |= (1 << CS10) | (1 << CS12); // Divide by 1024
    
    //OCR1A = 15624; // One second delay (when dividing by 1024).
    OCR1A = delay;
    
    TCCR1B |= (1 << WGM12); // Put timer into CTC mode
    TIMSK1 |= (1 << OCIE1A); // Enable the interrupt
    
    reset_fets();
    
    on = 1;
    mosfet = 0;
    sei();
}

void disable_display(void) {
    TIMSK1 &= ~(1 << OCIE1A);
    shift_clear();
    on = 0;
}

uint8_t display_on(void) {
    return on;
}


ISR(TIMER1_COMPA_vect) {
    
    uint8_t data[2];
    //uint8_t i;

    //data[0] = degree[bitPosition * 2];
    //data[1] = degree[bitPosition * 2 + 1];
   
    

    // Set the data to display
    switch (mode) {
        case 0: // Mode 0 - data from program memory
        case 1: // Mode 1 - data from program memory
            data[0] = read_byte(position);
            data[1] = read_byte(position + 1);
            break;
        case 2: // Mode 2 - data is hard coded
            data[0] = 255;
            data[1] = 255;
            break;
        case 3: // Mode 3 - data is hard coded
            data[0] = (mosfet << 7);
            data[1] = 0;
            break;
        case 4: // Mode 4 - data needs to be generated based on info.
            // Get distance travelled...
            // Get speed...
            data[0] = 0;
            data[1] = 0;
            break;
        default:
            data[0] = 0;
            data[1] = 0;
    }
    
    
    // Display it.
    output_data(data);
    
    // Make any modifications to the interrupt.
    bitPosition += mosfet;
    
    OCR1A <<= mosfet;
    mosfet ^= 1;
    
    if (bitPosition == ACCURACY) {
        bitPosition = 0;
        OCR1A = delay;
        
        // Set the data for the next degree:
        //for (i = 0; i < )
    }
    
    // Increase position. Position wraps around to 0.
    position += 2;
    if (position == (360 * ACCURACY)) position = 0;
}