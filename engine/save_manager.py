# engine/save_manager.py - COMPLETE REPLACEMENT
import json
import os
import time
from typing import Dict, Optional
from engine.state_manager import GameState

SAVE_VERSION = "1.1.0"
SAVES_DIR = "saves"
os.makedirs(SAVES_DIR, exist_ok=True)

class SaveManager:
    @staticmethod
    def save_game(game_state: GameState, scene_id: str, slot: int = 1) -> bool:
        save_data = {
            "version": SAVE_VERSION,
            "timestamp": time.time(),
            "scene_id": scene_id,
            "state": game_state.snapshot(),
            "checksum": hash(str(game_state.snapshot()))
        }

        path = os.path.join(SAVES_DIR, f"slot_{slot}.json")
        try:
            with open(path, "w") as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False

    @staticmethod
    def load_game(slot: int = 1) -> Optional[Dict]:
        path = os.path.join(SAVES_DIR, f"slot_{slot}.json")
        if not os.path.exists(path):
            return None

        try:
            with open(path, "r") as f:
                data = json.load(f)

            # Version check (future-proof)
            if data.get("version") != SAVE_VERSION:
                print("Save incompatible with current version")
                return None

            return data
        except Exception as e:
            print(f"Load failed: {e}")
            return None

    @staticmethod
    def delete_save(slot: int = 1):
        path = os.path.join(SAVES_DIR, f"slot_{slot}.json")
        if os.path.exists(path):
            os.remove(path)
