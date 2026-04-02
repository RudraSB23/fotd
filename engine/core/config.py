import json
import os

class Config:
    def __init__(self):
        self.data = {
            "debug": {"test_mode": False, "skip_startup": False},
            "display": {"typing_speed": 0.03, "glitch_intensity": 0.15},
            "audio": {"master_volume": 0.8, "music_volume": 0.5, "enable_music": True, "enable_sounds": True},
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

    def save(self):
        try:
            with open("config.json", "w") as f:
                json.dump(self.data, f, indent=4)
        except:
            pass

    @property
    def TEST(self):
        return self.data["debug"]["test_mode"]

    @TEST.setter
    def TEST(self, value):
        self.data["debug"]["test_mode"] = value

    @property
    def SKIP_STARTUP(self):
        return self.data["debug"]["skip_startup"]

    @SKIP_STARTUP.setter
    def SKIP_STARTUP(self, value):
        self.data["debug"]["skip_startup"] = value


    # Add getters for other values as needed
    @property
    def TYPING_SPEED(self):
        return self.data["display"]["typing_speed"]

    @property
    def SKIP_ANIMATIONS(self):
        return self.data["accessibility"]["skip_animations"]

    @SKIP_ANIMATIONS.setter
    def SKIP_ANIMATIONS(self, value):
        self.data["accessibility"]["skip_animations"] = value
        self.save()

    @property
    def ENABLE_MUSIC(self):
        return self.data["audio"].get("enable_music", True)

    @ENABLE_MUSIC.setter
    def ENABLE_MUSIC(self, value):
        self.data["audio"]["enable_music"] = value
        self.save()

    @property
    def ENABLE_SOUNDS(self):
        return self.data["audio"].get("enable_sounds", True)

    @ENABLE_SOUNDS.setter
    def ENABLE_SOUNDS(self, value):
        self.data["audio"]["enable_sounds"] = value
        self.save()

config = Config()