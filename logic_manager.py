 import json

class KarasuLogic:
    def __init__(self):
        self.config_file = "config.json"
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except:
            # ค่าเริ่มต้นตามสเปคโครงการ [cite: 40, 75]
            return {
                "volume": 15,
                "last_track": 1,
                "queue": [1, 2, 3, 4, 5],
                "mode": "normal" # normal, shuffle, repeat 
            }

    def save_data(self):
        with open(self.config_file, "w") as f:
            json.dump(self.data, f)

    def add_to_queue(self, track_number):
        """เพิ่มเพลงเข้าคิว (Lock/Move-Up Logic) [cite: 75, 82]"""
        if track_number not in self.data["queue"]:
            self.data["queue"].append(track_number)
            self.save_data()
            print(f"Track {track_number} added to queue.")

    def move_up(self, track_number):
        """ดันเพลงขึ้นลำดับหน้าสุด [cite: 30, 82]"""
        if track_number in self.data["queue"]:
            self.data["queue"].remove(track_number)
            self.data["queue"].insert(0, track_number)
            self.save_data()
            print(f"Track {track_number} moved to front.")

    def get_next_track(self):
        """หาเพลงถัดไปตามโหมด [cite: 81, 82]"""
        if not self.data["queue"]:
            return self.data["last_track"]
            
        next_t = self.data["queue"].pop(0)
        self.data["last_track"] = next_t
        self.save_data()
        return next_t