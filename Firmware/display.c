

#include "display.h"


/**
 * Access the mode variable from main so that we know what we should be
 * displaying.
 */
extern volatile uint8_t mode;

/**
 * Our position in the rotation - used to find which address to use when 
 * reading from program memory.
 */
volatile uint16_t position = ADDRESS_OFFSET;

/**
 * A flag that stores the state of the mosfets - 0 indicates FET1 is on and 
 * FET 2 is off, 1 indicates that FET1 is off and FET2 is on.
 */
volatile uint8_t mosfet = 0;

/**
 * Flag which stores whether or not the display is turned on.
 */
volatile uint8_t on = 0;

/**
 * Access the delay variable from the hall effect module so that we know based
 * on the current speed how long we need to wait between "columns" of data so
 * that the whole image is shown in a single revolution.
 */
extern volatile uint16_t delay;

/**
 * The speed of the wheel in metres per second, to two decimal places, 
 * separated into digits (e.g. 3.06 m/s would be {3, 0, 6}).
 */
volatile uint8_t speedDigits[3];

/**
 * The distance travelled, in metres, separated into digits (e.g. 105 metres
 * would be {0, 0, 1, 0, 5}.
 */
volatile uint8_t distanceDigits[5];

/**
 * A global variable for holding the speed display data as each column of data
 * is repeated 16 times per revolution.
 */
volatile uint8_t tempSpeedDisplayData;

/**
 * A global variable for holding the distance display data as each column of 
 * data is repeated 16 times per revolution.
 */
volatile uint8_t tempDistanceDisplayData;

/**
 * Hard coded data to be sent to the shift registers in order to output digits
 * 0 to 9 for the live speed/distance display mode.
 */
const uint8_t digitData[30] = {
        124, 68, 124,       // Zero
        0, 124, 0,          // One
        92, 84, 116,        // Two
        84, 84, 124,        // Three
        112, 16, 124,       // Four
        116, 84, 92,        // Five
        124, 84, 92,        // Six
        64, 64, 124,        // Seven
        124, 84, 124,       // Eight
        112, 80, 124        // Nine
};

/**
 * Hard coded data to be sent to the shift registers in order to output "m/s"
 * for the live speed/distance display mode.
 */
const uint8_t textData[18] = {
        0,
        124, 32, 16, 32, 124,   // m
        0,
        4, 8, 16, 32, 64,       // /
        0,
        116, 84, 84, 84, 92     // s
};


void RWW_SECTION enable_display(void) {

    cli();
    
    // Divide clock by 1 on timer1 (no prescaler).
    TCCR1B |= (1 << CS10);

    // Put timer1 into CTC mode (output compare mode).
    TCCR1B |= (1 << WGM12);
   
    // Indicate we are at the start of a revolution (sets the delay, resets
    // position, resets the timer, etc.
    start_revolution();
    
    on = 1;
    
    // Enable the output compare interrupt on timer1.
    TIMSK1 |= (1 << OCIE1A);

    sei();
}


void RWW_SECTION disable_display(void) {
    // Disable the output compare interrupt.
    TIMSK1 &= ~(1 << OCIE1A);
    
    // Clear the shift registers (turn of all LEDs).
    shift_clear();
    
    // Set on to zero.
    on = 0;
}


uint8_t RWW_SECTION display_on(void) {
    return on;
}


void RWW_SECTION start_revolution(void) {
    
    // Reset MOSFETs.
    reset_fets();
    mosfet = 0;
    
    // Reset position.
    position = ADDRESS_OFFSET;
    
    // Reset timer1.
    TCNT1 = 0;
    
    // Set delay from the hall effect delay variable.
    OCR1A = delay;
    
    // If we are in live speed/distance mode, get the speed and distance.
    if (mode == 4) {
        // Get speed and distance to be displayed.
        uint16_t speed = get_speed();
        uint32_t distance = get_distance();
        
        // Separate speed into digits.
        speedDigits[0] = speed/100;
        speed -= speedDigits[0] * 100;
        speedDigits[1] = speed/10;
        speed -= speedDigits[1]*10;
        speedDigits[2] = speed;
        
        // Separate distance into digits.
        distanceDigits[0] = distance/10000;
        distance -= distanceDigits[0];
        distanceDigits[1] = distance/1000;
        distance -= distanceDigits[1];
        distanceDigits[2] = distance/100;
        distance -= distanceDigits[2];
        distanceDigits[3] = distance/10;
        distance -= distanceDigits[3];
        distanceDigits[4] = distance;
    }
}


uint8_t RWW_SECTION get_speed_display_data(void) {
    
    // Nothing is displayed except in the centre of the image.
    if (position < 4768 + ADDRESS_OFFSET ||
            position >= 6752 + ADDRESS_OFFSET) {
        return 0;
    }
    
    // Calculate new display data at the beginning of every column of pixels -
    // each column typically has 32 bytes of data if we are displaying in
    // grayscale but given we are just displaying full brightness we only need
    // to recalculate at the start of the column and this data is repeated.
    if ((position % 32) < 4) {
        
        // Find our column position in the display
        uint16_t pos = (position - 4768 - ADDRESS_OFFSET)/32;
        
        if (pos < 6) {
            // First 6 pixels display the first digit of our speed.
            tempSpeedDisplayData = digitData[speedDigits[0] * 3 + pos/2];
        } else if (pos > 7 && pos < 10) {
            // Display a decimal place after the first digit of speed.
            tempSpeedDisplayData = 4;
        } else if (pos > 11 && pos < 18) {
            // Display the second digit of our speed.
            tempSpeedDisplayData = digitData[speedDigits[1] * 3 +
                    (pos - 12)/2];
        } else if (pos > 19 && pos < 26) {
            // Display the third digit of our speed.
            tempSpeedDisplayData = digitData[speedDigits[2] * 3 +
                    (pos - 20) / 2];
        } else if (pos > 25 && pos < 62) {
            // Display "m/s"
            tempSpeedDisplayData = textData[(pos - 26)/2];
        } else {
            // Display spaces.
            tempSpeedDisplayData = 0;
        }
    }
    
    return tempSpeedDisplayData >> mosfet;
}

uint8_t RWW_SECTION get_distance_display_data(void) {
    
    // Nothing is displayed except in the centre of the image.
    if (position < 4896 + ADDRESS_OFFSET ||
            position >= 6624 + ADDRESS_OFFSET) {
        return 0;
    }
    
    // Calculate new display data at the beginning of every column of pixels -
    // each column typically has 32 bytes of data if we are displaying in
    // grayscale but given we are just displaying full brightness we only need
    // to recalculate at the start of the column and this data is repeated.
    if ((position % 32) < 4) {
        
        // Find our column position in the display
        uint16_t pos = (position - 4896 - ADDRESS_OFFSET)/32;
        
        if (pos < 6) {
            // Display the first digit of distance.
            tempDistanceDisplayData = digitData[distanceDigits[0] * 3 + pos/2];
        } else if (pos > 7 && pos < 14) {
            // Display the second digit of distance.
            tempDistanceDisplayData = digitData[distanceDigits[1] * 3 +
                    (pos - 8)/2];
        } else if (pos > 15 && pos < 22) {
            // Display the third digit of distance.
            tempDistanceDisplayData = digitData[distanceDigits[2] * 3 +
                    (pos - 16)/2];
        } else if (pos > 23 && pos < 30) {
            // Display the fourth digit of distance.
            tempDistanceDisplayData = digitData[distanceDigits[3] * 3 +
                    (pos - 24)/2];
        } else if (pos > 31 && pos < 38) {
            // Display the fifth digit of distance.
            tempDistanceDisplayData = digitData[distanceDigits[4] * 3 +
                    (pos - 32)/2];
        } else if (pos > 41 && pos < 54) {
            // Display "m".
            tempDistanceDisplayData = textData[(pos - 42)/2];
        } else {
            // Display spaces.
            tempDistanceDisplayData = 0;
        }
    }
    
    return tempDistanceDisplayData >> mosfet;
}


/**
 * Interrupt service routine for LED driving. Although this would be neater
 * using functions from shift.c, it has instead been hard coded to avoid 
 * function calls so the the number of clock cycles this routine takes is
 * minimised.
 */
ISR(TIMER1_COMPA_vect) {
    
    uint8_t data[2];
    
    // Set output data based on current mode.
    if (mode == 0 || mode == 1) {
        data[0] = read_byte(position);
        data[1] = read_byte(position + 1);
    } else if (mode == 2) {
        data[0] = 255;
        data[1] = 255;
    } else if (mode == 3) {
        data[0] = (mosfet << 7);
        data[1] = 0;
    } else {
        // Assume we are in live speed/distance display mode.
        data[0] = get_speed_display_data();
        data[1] = get_distance_display_data();
    }
    
    // Output data
    shift_data_in(data[0]);
    shift_data_in(data[1]);
    toggle_latch_fets();
    toggle_latch();
    
    // Toggle the mosfet flag.
    mosfet ^= 1;

    // Increase position. Position wraps around to 0.
    position += 2;
    if (position == (11520 + ADDRESS_OFFSET)) position = ADDRESS_OFFSET;
}