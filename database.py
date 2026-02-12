import json
import os

# ชื่อไฟล์ที่จะเก็บข้อมูลใน Flash Memory 
DB_FILE = "config.json"

# ค่าเริ่มต้นของระบบ Karasu Box [cite: 40, 41, 75]
default_config = {
    "volume": 15,          # ระดับเสียงเริ่มต้น [cite: 40]
    "mode": "normal",      # โหมดการเล่น (normal, shuffle, repeat) [cite: 82, 92]
    "last_track": 1,       # เพลงล่าสุดที่เล่น [cite: 75]
    "queue": [1, 2, 3, 4, 5] # รายการคิวเพลง (Queue Manager) [cite: 75, 81]
}

def save_config(data):
    """บันทึกข้อมูลลงในหน่วยความจำแฟลช """
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f)
        print("Karasu Status: Saved to Flash")
    except Exception as e:
        print("Karasu Error (Save):", e)

def load_config():
    """ดึงข้อมูลจากหน่วยความจำแฟลช ถ้าไม่มีให้ใช้ค่าเริ่มต้น """
    try:
        if DB_FILE in os.listdir():
            with open(DB_FILE, "r") as f:
                return json.load(f)
        else:
            save_config(default_config) # สร้างไฟล์ครั้งแรก [cite: 75]
            return default_config
    except Exception as e:
        print("Karasu Error (Load):", e)
        return default_config