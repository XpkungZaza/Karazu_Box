from machine import Pin, UART
import time

# --- 1. ตั้งค่าการเชื่อมต่อ (UART) ---
# Pico GP0 (TX) --> ต่อเข้า RX ของ DFPlayer
# Pico GP1 (RX) --> ต่อเข้า TX ของ DFPlayer
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# --- 2. ตั้งค่าปุ่มกด (SW1 - SW4) ---
# ใช้ชื่อ sw1, sw2, sw3, sw4 ตรงๆ ไม่งง
sw1 = Pin(10, Pin.IN, Pin.PULL_UP)   # Play
sw2 = Pin(11, Pin.IN, Pin.PULL_UP)   # Pause
sw3 = Pin(12, Pin.IN, Pin.PULL_UP)   # Back 
sw4 = Pin(13, Pin.IN, Pin.PULL_UP)   # Next 

# ตัวแปรเก็บลำดับเพลงปัจจุบัน
current_track = 1
total_tracks = 20
is_paused = False  # <--- เพิ่มบรรทัดนี้เพื่อกำหนดสถานะเริ่มต้น [cite: 82]

# --- ฟังก์ชันส่งคำสั่งไป DFPlayer ---
def send_cmd(cmd, param1=0, param2=0):
    # คำนวณ Checksum เพื่อความถูกต้องของข้อมูล
    version = 0xFF
    length = 0x06
    feedback = 0x00
    checksum = 0 - (version + length + cmd + feedback + param1 + param2)
    high_check = (checksum >> 8) & 0xFF
    low_check = checksum & 0xFF

    packet = bytearray([
        0x7E, version, length, cmd, feedback,
        param1, param2, high_check, low_check, 0xEF
    ])
    uart.write(packet)
    time.sleep(0.1)

# --- ฟังก์ชันเริ่มต้นระบบ ---
def init_player():
    print("System Starting...")
    time.sleep(2)      # รอ DFPlayer ตื่น
    
    send_cmd(0x0C, 0, 0) # Reset โมดูล
    time.sleep(2)      # รอ Reset เสร็จ
    
    send_cmd(0x06, 0, 25) # ตั้งความดังเสียง (Level 20)
    time.sleep(0.5)
    print("Ready! (SW1=Play, SW2=Pause, SW3=Back, SW4=Next)")

# --- ฟังก์ชันควบคุม ---
def play_track(num):
    global current_track
    current_track = num
    # กันไม่ให้เลขเพลงหลุดขอบ (เช่น น้อยกว่า 1 หรือ มากกว่า 8)
    if current_track > total_tracks: current_track = 1
    if current_track < 1: current_track = total_tracks
    
    print(f"Playing Track: {current_track}")
    # คำสั่ง 0x03: เล่นเพลงตามลำดับไฟล์ (Root folder)
    send_cmd(0x03, 0, current_track)

def pause_track():
    print("Paused")
    send_cmd(0x0E, 0, 0)

def resume_track():
    print("Resume / Play")
    # คำสั่ง 0x0D: เล่นต่อจากเดิม (Playback)
    send_cmd(0x0D, 0, 0) 

# --- เริ่มทำงาน ---
init_player()

# --- ลูปหลัก (รอรับปุ่ม) ---
while True:
    # 1. เช็คปุ่ม SW1 (Play/Resume)
    if sw1.value() == 0:
        if is_paused == True:     # ถ้าเครื่องหยุดอยู่
            resume_track()        # สั่งให้เล่นต่อจากจุดเดิม ⏯️
            is_paused = False
        else:                     # ถ้าเครื่องยังไม่ได้เริ่มเล่น หรืออยากเริ่มใหม่
            play_track(current_track) 
        time.sleep(0.3)

    # 2. เช็คปุ่ม SW2 (Pause) - แก้ไขให้เป็นปุ่มหยุด
    elif sw2.value() == 0:
        pause_track()             # สั่งหยุดเพลงชั่วคราว ⏸️
        is_paused = True          # จำสถานะว่าหยุดอยู่
        time.sleep(0.3)

    # 3. เช็คปุ่ม SW3 (Back)
    elif sw3.value() == 0:
        current_track -= 1
        play_track(current_track) 
        is_paused = False         # เมื่อเปลี่ยนเพลง ให้ถือว่าไม่ได้หยุดอยู่
        time.sleep(0.3)

    # 4. เช็คปุ่ม SW4 (Next)
    elif sw4.value() == 0:
        current_track += 1
        play_track(current_track) 
        is_paused = False 
        time.sleep(0.3)

    time.sleep(0.05) # พัก CPU เล็กน้อย 🧠