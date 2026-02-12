from machine import Pin, I2C
import ssd1306

class UIManager:
    def __init__(self, sda_pin=0, scl_pin=1):
        # ตั้งค่า I2C (ปรับเลขขาตามที่เพื่อนต่อจริงนะ)
        self.i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c) [cite: 32, 76]

    def display_home(self, data):
        """หน้าจอหลัก: แสดงชื่อเพลง ระดับเสียง และสถานะ"""
        self.oled.fill(0) # ล้างหน้าจอ
        
        # ส่วนหัว (Header)
        self.oled.text("Karasu Box", 25, 0) [cite: 4]
        self.oled.line(0, 10, 128, 10, 1) 
        
        # ส่วนแสดงผลเพลง (Body)
        self.oled.text("Track: {:04d}".format(data['last_track']), 0, 20) [cite: 31, 47]
        self.oled.text("Vol: " + str(data['volume']), 0, 35) [cite: 40]
        self.oled.text("Mode: " + data['mode'], 0, 50) [cite: 75, 82]
        
        # แถบแบตเตอรี่ (จำลองไว้ก่อน)
        self.oled.rect(100, 50, 25, 12, 1) [cite: 36, 76]
        
        self.oled.show()