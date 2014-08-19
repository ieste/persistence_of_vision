#define LATCH 4    // Green
#define CLOCK 3    // Yellow
#define DATA 2     // Blue
#define SHIFT_REG PORTD
#define SHIFT_DIR DDRD

#include <util/delay.h>

void setup() {
  // Set the Latch, Clock and Data lines as outputs.
  SHIFT_DIR |= (1 << LATCH) | (1 << CLOCK) | (1 << DATA);
  // Set the Latch, Clock and Data lines low.
  SHIFT_REG &= ~((1 << LATCH) | (1 << CLOCK) | (1 << DATA));
}

void loop() {
  shift_data_in(0b10101010);
  toggle_latch();
  _delay_ms(2000);
  shift_data_in(0b01010101);
  toggle_latch();
  _delay_ms(2000);

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
shift_data_in (char data)
{
  char i = 0;

  for (i = 7; i >= 0; i--)
  {
    if ((data >> i) & 1)
      SHIFT_REG |= (1 << DATA);
    else
      SHIFT_REG &= (~(1 << DATA));

    SHIFT_REG ^= (1 << CLOCK);
    _delay_us(1);
    SHIFT_REG ^= (1 << CLOCK);
  }

  SHIFT_REG &= (~(1 << LATCH));
}


