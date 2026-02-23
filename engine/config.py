import json
import os

class Config:
    def __init__(self):
        self.data = {
            "debug": {"test_mode": False, "skip_startup": False},
            "display": {"typing_speed": 0.03, "glitch_intensity": 0.15},
            "audio": {"master_volume": 0.8, "music_volume": 0.5},
            "accessibility": {"high_contrast": False, "skip_animations": False}
        }
        self.load()

    def load(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json") as f:
                    self.data.update(json.load(f))
            except:
                pass

    @property
    def TEST(self):
        return self.data["debug"]["test_mode"]

    @property
    def SKIP_STARTUP(self):
        return self.data["debug"]["skip_startup"]

    # Add getters for other values as needed
    @property
    def TYPING_SPEED(self):
        return self.data["display"]["typing_speed"]

    @property
    def ENABLE_MUSIC(self):
        return True # Default to True, can be mapped to self.data if needed

    @property
    def ENABLE_SOUNDS(self):
        return True # Default to True

config = Config()