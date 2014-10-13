/*
*   SHIFT_TEST.c
*   Created by Isabella Stephens on 19/08/2014.
*
*   For the ATMega328P
*
*   PC5 Blue Serial Data Line
*   PC4 Green ST_CP Latch Line
*   PC3 Yellow SH_CP Clock Line
*   Toggle LEDs attached to a shift register: 74HC595
*/

#define F_CPU 16000000UL     // 16 MHz

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h> // These delay functions do not appear to give
                        // reliable delays. Internal clock used instead.


#define LATCH 3     // Green
#define CLOCK 4     // Yellow
#define DATA 5      // Blue
#define FET2 2      // White
#define FET1 1      // White
#define SHIFT_REG PORTC
#define SHIFT_DIR DDRC

void clockInit(void);
void shift_data_in (uint8_t data);
void toggle_latch (void);
void ledInit(void);

volatile uint8_t flag;
volatile uint8_t fet;
volatile uint8_t bytesRemaining;
volatile uint8_t ds[8][16];
volatile uint8_t dataSent;
volatile uint8_t d[2][15] = {{0, 1, 1, 3, 3, 7, 7, 15, 15, 31, 31, 63, 63, 127, 127}, {1, 1, 3, 3, 7, 7, 15, 15, 31, 31, 63, 63, 127, 127, 255}};



int
main(void)
{
    ledInit();
    
    clockInit();
    
    sei();
    
    flag = 0;
    fet = 0;
    dataSent = 0;
    
    while (1) {} // Loop indefinitely
}

void ledInit(void) {
    // Set the Latch, Clock and Data lines as outputs.
    SHIFT_DIR |= (1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << FET1) |
    (1 << FET2);
    
    // Set the Latch, Clock and Data lines low. Also MOSFET 2.
    SHIFT_REG &= ~((1 << LATCH) | (1 << CLOCK) | (1 << DATA) | (1 << FET2));
    
    // Set MOSFET 1 high.
    SHIFT_REG |= (1 << FET1);
    
    DDRD |= 1;
    PORTD &= ~(1);
}

void
toggle_latch (void)
{
    // Delay for 100 ns to ensure latching succeeds.
    _delay_us(1);
    // Toggle the latch.
    SHIFT_REG ^= (1 << LATCH);
    
    
}

void
shift_data_in (uint8_t data)
{
    
    for (uint8_t i = 0; i < 8; i++)
    {
        if (((data >> (7 - i)) & 1))
            SHIFT_REG |= (1 << DATA);
        else
            SHIFT_REG &= (~(1 << DATA));
        
        SHIFT_REG ^= (1 << CLOCK);
        _delay_us(1);
        SHIFT_REG ^= (1 << CLOCK);
    }
    
    toggle_latch();
}

void
clockInit (void)
{
    cli();  // disable interrupts while setting up
    TCCR1B |= (1 << CS12) | (1 << CS10);    // Divide clock by 1024
    OCR1A = 2;  // 1 Second (15624) //8
    TCCR1B |= (1 << WGM12); // Put timer into CTC mode
    TIMSK1 |= (1 << OCIE1A); // Enable the timer compare interrupt
    sei();  // enable interrupts
}

//interrupt service routine for timer
ISR(TIMER1_COMPA_vect)
{
    if (flag == 15) flag = 0;

    toggle_latch();
    shift_data_in(d[fet][flag]);
    
    // Toggle the mosfet.
    SHIFT_REG ^= (1 << FET1) | (1 << FET2);
    
    fet ^= 1;
    flag += fet;
}

