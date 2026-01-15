import customtkinter as ctk
import serial
import serial.tools.list_ports
import threading
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- CONFIG ---
PICO_VID = 0x2E8A
BAUD_RATE = 115200

class VolumeControllerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pico Volume & LCD")
        self.geometry("400x450")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.running = True
        self.serial_conn = None
        self.volume_interface = self.init_audio()
        self.current_vol = 0

        # --- GUI ELEMENTS ---
        self.lbl_title = ctk.CTkLabel(self, text="Pico Control Deck", font=("Roboto Medium", 22))
        self.lbl_title.pack(pady=15)

        # Volume Section
        self.lbl_percent = ctk.CTkLabel(self, text="0%", font=("Roboto", 40))
        self.lbl_percent.pack(pady=5)
        
        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.set(0)
        self.progress.pack(pady=10)

        # LCD Text Section
        self.lbl_lcd = ctk.CTkLabel(self, text="LCD Message:", font=("Roboto", 14))
        self.lbl_lcd.pack(pady=(20, 5))

        self.entry_lcd = ctk.CTkEntry(self, width=200, placeholder_text="Type message here...")
        self.entry_lcd.pack(pady=5)

        self.btn_send = ctk.CTkButton(self, text="Send to LCD", command=self.send_to_lcd)
        self.btn_send.pack(pady=5)

        # Status Bar
        self.lbl_status = ctk.CTkLabel(self, text="Searching...", text_color="orange")
        self.lbl_status.pack(side="bottom", pady=10)

        # Start Thread
        self.thread = threading.Thread(target=self.serial_loop, daemon=True)
        self.thread.start()

    def init_audio(self):
        try:
            devices = AudioUtilities.GetDeviceEnumerator()
            interface = devices.GetDefaultAudioEndpoint(0, 1)
            vol = interface.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            return cast(vol, POINTER(IAudioEndpointVolume))
        except:
            return None

    def send_to_lcd(self):
        """Send the text box content to the Pico"""
        text = self.entry_lcd.get()
        # Ensure it's not too long (16 chars max recommended)
        text = text[:16] 
        if self.serial_conn and self.serial_conn.is_open:
            try:
                msg = f"MSG:{text}\n"
                self.serial_conn.write(msg.encode('utf-8'))
                self.lbl_status.configure(text="Message Sent!", text_color="#2CC985")
            except Exception as e:
                self.lbl_status.configure(text=f"Send Error: {e}", text_color="red")

    def find_pico(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == PICO_VID:
                return port.device
        return None

    def serial_loop(self):
        while self.running:
            port = self.find_pico()
            if port:
                self.lbl_status.configure(text=f"Connected: {port}", text_color="#2CC985")
                try:
                    with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
                        self.serial_conn = ser
                        ser.reset_input_buffer()
                        
                        while self.running:
                            if ser.in_waiting > 0:
                                try:
                                    line = ser.readline().decode('utf-8').strip()
                                    # We now look for the "VOL:" prefix
                                    if line.startswith("VOL:"):
                                        val_str = line.split(":")[1]
                                        val = int(val_str)
                                        
                                        # Update GUI
                                        self.lbl_percent.configure(text=f"{val}%")
                                        self.progress.set(val / 100)
                                        
                                        # Set Windows Volume
                                        if self.volume_interface:
                                            scalar = val / 100.0
                                            self.volume_interface.SetMasterVolumeLevelScalar(scalar, None)
                                            
                                except ValueError:
                                    pass
                            time.sleep(0.01)
                except Exception:
                    self.lbl_status.configure(text="Disconnected", text_color="red")
                    self.serial_conn = None
                    time.sleep(2)
            else:
                self.lbl_status.configure(text="Searching for Pico...", text_color="orange")
                time.sleep(2)

if __name__ == "__main__":
    app = VolumeControllerApp()
    app.mainloop()