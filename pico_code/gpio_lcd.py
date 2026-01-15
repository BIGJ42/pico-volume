import time
from machine import Pin
from lcd_api import LcdApi

class GpioLcd(LcdApi):
    def __init__(self, rs_pin, e_pin, d4_pin, d5_pin, d6_pin, d7_pin, num_lines=2, num_columns=16):
        self.rs = Pin(rs_pin, Pin.OUT)
        self.e = Pin(e_pin, Pin.OUT)
        self.d4 = Pin(d4_pin, Pin.OUT)
        self.d5 = Pin(d5_pin, Pin.OUT)
        self.d6 = Pin(d6_pin, Pin.OUT)
        self.d7 = Pin(d7_pin, Pin.OUT)
        
        # Determine Pin objects for data nibble
        self.d4.value(0)
        self.d5.value(0)
        self.d6.value(0)
        self.d7.value(0)
        self.rs.value(0)
        self.e.value(0)
        
        time.sleep(0.02)
        # Initialization sequence for 4-bit mode
        self.hal_write_init_nibble(0x03)
        time.sleep(0.005)
        self.hal_write_init_nibble(0x03)
        time.sleep(0.001)
        self.hal_write_init_nibble(0x03)
        self.hal_write_init_nibble(0x02)
        
        # Initialize API
        LcdApi.__init__(self, num_lines, num_columns)
        
        # Configure display
        self.hal_write_command(0x28) # 2 lines, 5x8 matrix
        self.hal_write_command(0x0C) # Display ON, Cursor OFF
        self.hal_write_command(0x06) # Increment cursor
        self.clear()

    def hal_write_init_nibble(self, nibble):
        self.hal_write_nibble(nibble)
        self.pulse_enable()

    def hal_write_nibble(self, nibble):
        self.d4.value((nibble >> 0) & 1)
        self.d5.value((nibble >> 1) & 1)
        self.d6.value((nibble >> 2) & 1)
        self.d7.value((nibble >> 3) & 1)

    def hal_write_byte(self, byte):
        self.hal_write_nibble(byte >> 4)
        self.pulse_enable()
        self.hal_write_nibble(byte & 0x0F)
        self.pulse_enable()

    def hal_write_command(self, cmd):
        self.rs.value(0)
        self.hal_write_byte(cmd)
        time.sleep(0.002)

    def hal_write_data(self, data):
        self.rs.value(1)
        self.hal_write_byte(data)

    def pulse_enable(self):
        self.e.value(1)
        time.sleep_us(1)
        self.e.value(0)
        time.sleep_us(50)

    def impl_init(self):
        # Already handled in __init__
        pass

    def impl_clear(self):
        self.hal_write_command(0x01)
        time.sleep(0.002)

    def impl_putchar(self, char):
        self.hal_write_data(ord(char))

    def impl_move_to(self, cursor_x, cursor_y):
        addr = 0x80 + cursor_x + (0x40 * cursor_y)

        self.hal_write_command(addr)
