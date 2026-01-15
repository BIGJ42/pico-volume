# Pico Volume Slider & LCD Deck

A custom hardware volume mixer built with a Raspberry Pi Pico, a Slide Potentiometer, and a 16x2 LCD display. This project allows you to control your Windows master volume with a physical fader, view the volume level in real-time on the LCD, and send custom text messages from your PC to the hardware display.

## 🌟 Features
*   **Analog Volume Control:** Smooth linear fader control mapped to Windows Master Volume.
*   **Real-time LCD Feedback:** Visual progress bar and percentage display on a 1602 LCD.
*   **Bidirectional Sync:** The PC software listens to the slider, but also sends data back to the LCD.
*   **Custom Messaging:** Send text from the PC GUI directly to the hardware screen.
*   **Auto-Calibration:** Software compensation ensures the slider hits a perfect 0% and 100%.

## 🛠️ Hardware Requirements
*   **Raspberry Pi Pico**
*   **Slide Potentiometer** (Linear/B10k recommended)
*   **16x2 LCD Display** (Standard Parallel Interface)
*   **Resistors:**
    *   220Ω (For LCD Backlight)
    *   2kΩ + 220Ω (For LCD Contrast Voltage Divider) - *Or a 10k Potentiometer*
*   Jumper Wires & Breadboard/PCB

## 🔌 Wiring Guide

### Slide Potentiometer
| Pot Pin | Pico Pin |
| :--- | :--- |
| **VCC** | 3V3 (Pin 36) |
| **GND** | GND (Pin 38) |
| **Output** | GP26 (Pin 31) |

### LCD Display (Parallel Mode)
*Note: This uses the 4-bit GPIO method, not I2C.*

| LCD Pin | Function | Pico Pin / Connection |
| :--- | :--- | :--- |
| **1 (VSS)** | GND | GND |
| **2 (VDD)** | 5V Power | VBUS (Pin 40) |
| **3 (V0)** | Contrast | **Voltage Divider:** Connect 2kΩ to 5V and 220Ω to GND. Connect both to Pin 3. |
| **4 (RS)** | Register Select | GP0 (Pin 1) |
| **5 (RW)** | Read/Write | GND |
| **6 (E)** | Enable | GP1 (Pin 2) |
| **11 (D4)** | Data 4 | GP2 (Pin 4) |
| **12 (D5)** | Data 5 | GP3 (Pin 5) |
| **13 (D6)** | Data 6 | GP4 (Pin 6) |
| **14 (D7)** | Data 7 | GP5 (Pin 7) |
| **15 (A)** | Backlight (+) | 220Ω Resistor -> VBUS (Pin 40) |
| **16 (K)** | Backlight (-) | GND |

## 💾 Installation

### 1. Pico Setup
1.  Plug in your Pico while holding the **BOOTSEL** button.
2.  Install the [MicroPython UF2 firmware](https://micropython.org/download/rp2-pico/).
3.  Open **Thonny IDE**.
4.  Upload the three files found in the `pico_code` folder of this repository to the root of the Pico:
    *   `lcd_api.py` (Driver)
    *   `gpio_lcd.py` (Driver)
    *   `main.py` (Main Logic)
5.  **Restart the Pico.** The LCD should light up and display "System Ready".

### 2. PC Setup
You have two options to run the PC software:

#### Option A: The Easy Way (Exe)
1.  Go to the **[Releases](../../releases)** section of this repository.
2.  Download `script.exe`.
3.  Run it. (If Windows Defender warns you, click "More Info" -> "Run Anyway" - this is because the app isn't signed).

#### Option B: The Developer Way (Python Script)
1.  Clone this repository.
2.  Install the required libraries:
    ```bash
    pip install customtkinter pyserial pycaw comtypes
    ```
3.  Run the script:
    ```bash
    python script.py
    ```

## 🎮 How to Use
1.  **Connect:** Plug in the Pico via USB.
2.  **Launch:** Open `script.exe` (or run `script.py`).
3.  **Status:** The app will automatically find the Pico and turn the status text **Green**.
4.  **Control:** Move the slider to change volume.
5.  **Message:** Type text into the box in the GUI and click **Send to LCD** to display it on the hardware screen.

## 🐛 Troubleshooting

*   **White Boxes on Screen / No Text:**
    *   Your contrast is too high. Ensure you have the resistors (2k + 220Ω) or a potentiometer connected correctly to LCD Pin 3 (V0).
*   **"Searching for Pico..." forever:**
    *   Make sure you are using a Data USB cable, not just a charging cable.
    *   Ensure Thonny is closed (Thonny blocks the connection).
*   **Volume stuck at 96%:**
    *   The `main.py` code includes a calibration zone. If your slider is old or dirty, you can adjust `MAX_RAW` in `main.py`.

## 📜 License
This project is open source. Feel free to modify and improve!
