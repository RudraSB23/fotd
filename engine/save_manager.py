import json
import os
from typing import Optional, Dict, Any
from engine.state_manager import GameState

SAVE_FILE = "saves.json"

class SaveManager:
    @staticmethod
    def save_game(state: GameState, current_scene: str, stdscr=None):
        """Saves current GameState and scene location to a JSON file."""
        data = {
            "player_name": state.player_name,
            "identity_fragments": state.identity_fragments,
            "corruption_level": state.corruption_level,
            "stability": state.stability,
            "npc_relationships": state.npc_relationships,
            "current_node_id": state.current_node_id,
            "current_scene": current_scene
        }
        try:
            # Ensure the directory exists (even though it's root, good practice)
            directory = os.path.dirname(SAVE_FILE)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            
            # Visual Indicator if stdscr is provided
            if stdscr:
                from engine.console_effects import Colors, print_colored
                import time
                
                # Save current cursor position
                orig_y, orig_x = stdscr.getyx()
                
                h, w = stdscr.getmaxyx()
                msg = "[ SAVING... ]"
                # Bottom right corner
                msg_x = w - len(msg) - 1
                msg_y = h - 1
                
                # Render indicator
                print_colored(msg, Colors.BOLD_GREEN, stdscr=stdscr, y=msg_y, x=msg_x, end="")
                stdscr.refresh()
                
                time.sleep(1.5)
                
                # Clear indicator (overwrite with spaces)
                stdscr.addstr(msg_y, msg_x, " " * len(msg))
                
                # Restore original cursor position
                stdscr.move(orig_y, orig_x)
                stdscr.refresh()

            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    @staticmethod
    def load_game() -> Optional[Dict[str, Any]]:
        """Loads and returns save data dictionary if it exists."""
        if not os.path.exists(SAVE_FILE):
            return None
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    @staticmethod
    def delete_save():
        """Deletes the local save file."""
        if os.path.exists(SAVE_FILE):
            try:
                os.remove(SAVE_FILE)
                return True
            except Exception as e:
                print(f"Error deleting save: {e}")
        return False

    @staticmethod
    def restore_state(data: Dict[str, Any]) -> GameState:
        """Constructs a GameState object from loaded data."""
        state = GameState()
        state.player_name = data.get("player_name", "Unknown")
        state.identity_fragments = data.get("identity_fragments", [])
        state.corruption_level = data.get("corruption_level", 0)
        state.stability = data.get("stability", 3)
        state.npc_relationships = data.get("npc_relationships", {})
        state.current_node_id = data.get("current_node_id", "intro")
        return state
