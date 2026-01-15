from machine import ADC, Pin
import time
import sys
import uselect

# --- CONFIG ---
SLIDER_PIN = 26

# --- SETUP SLIDER ---
slider = ADC(Pin(SLIDER_PIN))

# --- SETUP LCD ---
lcd = None
try:
    from gpio_lcd import GpioLcd
    # Pin definitions based on your wiring
    lcd = GpioLcd(rs_pin=0, e_pin=1, d4_pin=2, d5_pin=3, d6_pin=4, d7_pin=5)
    lcd.clear()
    lcd.putstr("Pico Audio")
    lcd.move_to(0, 1)
    lcd.putstr("Init OK")
    print("LCD Init Success")
except Exception as e:
    print(f"LCD Failed: {e}")
    lcd = None

# --- SETUP SERIAL LISTENER ---
poll_obj = uselect.poll()
poll_obj.register(sys.stdin, uselect.POLLIN)

last_vol = -1

# --- CALIBRATION CONFIG ---
# This ensures 0% is 0 and 100% is 100
MIN_RAW = 2000
MAX_RAW = 62000

def update_lcd(vol):
    if not lcd: return
    try:
        # Create a visual bar like: Vol: 50% |||
        blocks = int((vol / 100) * 5)
        bar = "|" * blocks
        lcd.move_to(0, 0)
        # Pad with spaces to clear old text
        lcd.putstr(f"Vol:{vol}% {bar:<5}")
    except:
        pass

while True:
    # 1. READ SLIDER
    raw = slider.read_u16()
    
    # 2. CALIBRATION
    if raw < MIN_RAW: raw = MIN_RAW
    if raw > MAX_RAW: raw = MAX_RAW
    
    # Map raw value to 0-100
    vol = int((raw - MIN_RAW) * 100 // (MAX_RAW - MIN_RAW))
    
    # 3. PROCESS CHANGES
    if vol != last_vol:
        # Send to PC
        print(f"VOL:{vol}")
        # Update Screen
        update_lcd(vol)
        last_vol = vol
        
    # 4. CHECK FOR PC MESSAGES
    if poll_obj.poll(0):
        try:
            line = sys.stdin.readline().strip()
            if line.startswith("MSG:") and lcd:
                text = line[4:]
                lcd.move_to(0, 1)
                lcd.putstr(f"{text:<16}")
        except:
            pass

    time.sleep(0.05)
