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
total_tracks = 20  # มีเพลง 0001.mp3 ถึง 0008.mp3

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
    
    send_cmd(0x06, 0, 18) # ตั้งความดังเสียง (Level 20)
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
    # อ่านค่าปุ่ม (0 = กด, 1 = ไม่กด)
    
    if sw1.value() == 0:  # ปุ่ม PLAY
        if is_paused == True:     # ถ้ามันหยุดอยู่
            resume_track()        # สั่งเล่นต่อ (Resume)
            is_paused = False     # ยกเลิกสถานะจำ
        else:                     # ถ้าปกติ
            play_track(current_track) # เล่นเพลงเดิมซ้ำ (หรือเริ่มใหม่)
        
        time.sleep(0.3)

    elif sw2.value() == 0: # ปุ่ม PAUSE
        pause_track()
        is_paused = True   # <--- เพิ่มบรรทัดนี้: จำไว้ว่าตอนนี้หยุดอยู่นะ
        time.sleep(0.3)

    elif sw3.value() == 0: # ปุ่ม BACK 
        current_track -= 1
        play_track(current_track) # ส่งเล่นเพลงใหม่ทันที
        time.sleep(0.3)

    elif sw4.value() == 0: # ปุ่ม NEXT
        current_track += 1
        play_track(current_track) 
        is_paused = False  # <--- เพิ่มบรรทัดนี้: เปลี่ยนเพลงแล้ว เลิกจำว่า Pause ได้เลย
        time.sleep(0.3)

    time.sleep(0.05) # พักเครื่องนิดหน่อย
