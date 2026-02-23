import os
import pygame
import threading
from .config import config


class AudioManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(AudioManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        pygame.mixer.init()
        self.current_track = None
        self.sounds = {}
        self.sounds_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds")
        self.loading_complete = threading.Event()
        
        # Start preloading in the background
        self._load_thread = threading.Thread(target=self._preload_worker, daemon=True)
        self._load_thread.start()
        
        self._initialized = True

    def _preload_worker(self):
        self.preload_sounds()
        self.loading_complete.set()

    def wait_for_assets(self, timeout=None):
        """Wait for the background loading to complete."""
        return self.loading_complete.wait(timeout)

    def is_loading_finished(self):
        return self.loading_complete.is_set()

    # -----------------
    # PRELOAD
    # -----------------
    def preload_sounds(self):
        if not os.path.exists(self.sounds_dir):
            print(f"[WARN] Sounds directory not found: {self.sounds_dir}")
            return

        for file in os.listdir(self.sounds_dir):
            if file.lower().endswith((".mp3", ".wav")):
                self.load_sound(file)

    # -----------------
    # BACKGROUND MUSIC
    # -----------------
    def play_music(self, file: str, loop: bool = True, volume: float = 0.5):
        if not config.ENABLE_MUSIC:
            return  # music disabled

        path = os.path.join(self.sounds_dir, file)
        if not os.path.exists(path):
            print(f"[WARN] Music file not found: {path}")
            return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_track = path
        except Exception as e:
            print(f"[DEBUG] Music playback failed: {e}")
            pass

    def stop_music(self, fadeout_ms: int = 1000):
        if not config.ENABLE_MUSIC:
            return

        if fadeout_ms > 0:
            pygame.mixer.music.fadeout(fadeout_ms)
        else:
            pygame.mixer.music.stop()
        self.current_track = None

    def is_playing(self) -> bool:
        if not config.ENABLE_MUSIC:
            return False

        return pygame.mixer.music.get_busy()

    def set_volume(self, volume: float):
        if not config.ENABLE_MUSIC:
            return

        pygame.mixer.music.set_volume(volume)

    # -----------------
    # SOUND EFFECTS
    # -----------------
    def load_sound(self, file: str):
        if file in self.sounds:
            return self.sounds[file]

        path = os.path.join(self.sounds_dir, file)
        if not os.path.exists(path):
            return None

        try:
            self.sounds[file] = pygame.mixer.Sound(path)
        except Exception as e:
            return None
        return self.sounds[file]

    def play_sound(self, file: str, volume: float = 0.7, loop: bool = False):
        if not config.ENABLE_SOUNDS:
            return  # sounds disabled

        sound = self.sounds.get(file)
        if sound:
            sound.set_volume(volume)
            sound.play(-1 if loop else 0)

    def stop_sound(self, file: str):
        if not config.ENABLE_SOUNDS:
            return

        sound = self.sounds.get(file)
        if sound:
            sound.stop()
