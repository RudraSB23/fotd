# 🎮 Fragments of the Lattice – Complete Codebase Refactor & Implementation Prompt

**You are Antigravity, the expert Python game development agent. Your task is to systematically refactor and enhance the "Fragments of the Lattice" codebase based on the comprehensive audit.**

## 📋 Phase 1: Setup & Directory Analysis

### 1.1 Analyze Full Directory

```
1. Analyze the current directory
2. Run the game locally: python main.py
3. Document current folder structure, key files, and dependencies
```

**Create a `README_REFACTOR.md` documenting:**

- Current file structure
- Key classes and their responsibilities
- Current game flow (main.py → scenes)
- Assets structure (sounds, ASCII)

---

## 📋 Phase 2: Critical Architecture Fixes (Priority 1)

### 2.1 Enhanced GameState (File: `engine/state_manager.py`)

**Replace current GameState with this enhanced version:**

```python
# engine/state_manager.py - COMPLETE REPLACEMENT
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
import time
import json

def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))

@dataclass
class GameState:
    player_name: str = "Caretaker"
    identity_fragments: List[str] = field(default_factory=list)
    corruption_level: int = 0
    stability: int = 3
    npc_relationships: Dict[str, int] = field(default_factory=dict)
    current_node_id: str = "intro"
    history: List[Dict] = field(default_factory=list)
    puzzles_solved: int = 0
    puzzles_failed: int = 0
    nodes_visited: int = 0
    playtime_seconds: float = 0.0

    # STAT MANIPULATION - Type Safe
    def apply_stability(self, delta: int) -> None:
        old = self.stability
        self.stability = clamp(self.stability + delta, 0, 10)
        self.history.append({
            "type": "stability",
            "delta": delta,
            "old": old,
            "new": self.stability,
            "timestamp": time.time()
        })

    def apply_corruption(self, delta: int) -> None:
        old = self.corruption_level
        self.corruption_level = clamp(self.corruption_level + delta, 0, 10)
        self.history.append({
            "type": "corruption",
            "delta": delta,
            "old": old,
            "new": self.corruption_level,
            "timestamp": time.time()
        })

    def add_fragment(self, fragment_id: str) -> bool:
        if fragment_id not in self.identity_fragments:
            self.identity_fragments.append(fragment_id)
            self.history.append({
                "type": "fragment",
                "fragment_id": fragment_id,
                "timestamp": time.time()
            })
            return True
        return False

    def relationship_delta(self, npc: str, delta: int) -> None:
        self.npc_relationships[npc] = self.npc_relationships.get(npc, 0) + delta

    # UTILITY
    def snapshot(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.snapshot())

    @classmethod
    def from_snapshot(cls, data: Dict):
        return cls(**data)

    def get_ending(self) -> str:
        if self.corruption_level >= 8:
            return "collapse"
        elif self.stability >= 8:
            return "restoration"
        elif 3 <= self.corruption_level < 6 and 3 <= self.stability < 6:
            return "integration"
        return "undetermined"
```

**Legacy Compatibility Wrapper** (keep for now):

```python
    # TEMPORARY - for existing dialogue.py calls
    def apply_effect(self, effect_str: str) -> None:
        if effect_str.startswith("stability+"):
            self.apply_stability(int(effect_str.split("+"))) 
        elif effect_str.startswith("stability-"):
            self.apply_stability(-int(effect_str.split("-"))) 
        elif effect_str.startswith("corruption+"):
            self.apply_corruption(int(effect_str.split("+"))) 
        elif effect_str.startswith("corruption-"):
            self.apply_corruption(-int(effect_str.split("-"))) 
        elif effect_str.startswith("fragment:"):
            self.add_fragment(effect_str.split(":", 1)) 
```

### 2.2 Scene-Based Architecture

**Create new folder structure:**

```
scenes/
├── __init__.py
├── base_scene.py
├── registry.py
├── node_0x1_corridor.py
├── node_0x2_ava.py
└── utils.py
```

**scenes/base_scene.py:**

```python
from abc import ABC, abstractmethod
from engine.state_manager import GameState

class BaseScene(ABC):
    def __init__(self):
        self.scene_id = self.__class__.__name__.lower()

    @abstractmethod
    def run(self, stdscr, game_state: GameState) -> str:
        """Returns next scene_id or None to end game"""
        pass
```

**scenes/registry.py:**

```python
from .node_0x1_corridor import Scene1Corridor
from .node_0x2_ava import Scene2Ava

SCENE_REGISTRY = {
    "scene1_identity_sequence": Scene1Corridor,
    "node0x2_ava_intro": Scene2Ava,
    # Add future scenes here
}

def get_scene(scene_id: str):
    scene_class = SCENE_REGISTRY.get(scene_id)
    if scene_class:
        return scene_class()
    raise ValueError(f"Unknown scene: {scene_id}")
```

**Migrate FIRST scene** (`scene1_identity_sequence` and corridor logic) from `dialogue.py` to `scenes/node_0x1_corridor.py`. Keep the exact same narrative flow.

### 2.3 Robust Save System

**engine/save_manager.py - COMPLETE REPLACEMENT:**

```python
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
    delete_save(slot: int = 1):
        path = os.path.join(SAVES_DIR, f"slot_{slot}.json")
        if os.path.exists(path):
            os.remove(path)
```

### 2.4 Update main.py Save/Load Logic

**Replace the continue/new game logic in main.py:**

```python
# In main.py, replace the "Continue" block:
if choice_index == 0:  # Continue
    msg = [("SEARCHING FOR LOCAL FRAGMENTS...", Colors.BOLD_CYAN)]
    box = MessageBox(msg, title="SYSTEM SCAN", border_color=Colors.BOLD_CYAN)
    box.display(stdscr, duration=2.0)

    save_data = SaveManager.load_game(slot=1)
    if save_data:
        game_state = GameState.from_snapshot(save_data["state"])
        scene_id = save_data["scene_id"]

        try:
            next_scene = get_scene(scene_id)
            success_msg = [
                ("FRAGMENT RESTORED", Colors.BOLD_GREEN),
                "",
                f"Subject: {game_state.player_name}",
                f"Location: {scene_id}",
                "",
                ("Re-aligning consciousness...", Colors.BOLD_WHITE)
            ]
            box = MessageBox(success_msg, title="SYNC SUCCESS", border_color=Colors.BOLD_GREEN)
            box.display(stdscr, duration=2.0)

            next_scene.run(stdscr, game_state)
            return
        except ValueError as e:
            error_msg = [
                ("LINK CORRUPTION", Colors.BOLD_RED),
                "",
                f"Could not resolve scene: {scene_id}",
                "Data is unreadable.",
                "",
                ("Returning to primary node...", Colors.BOLD_WHITE)
            ]
            box = MessageBox(error_msg, title="NODE FAILURE", border_color=Colors.BOLD_RED)
            box.display(stdscr)
    # ... rest of error handling
```

**Test:** Create a save in Node 0x2, restart, load it, ensure it resumes correctly.

---

## 📋 Phase 3: Input & Error Handling Fixes

### 3.1 Global Input Flush Helper

**engine/ui_utils.py:**

```python
import curses

def flush_input_buffer(stdscr):
    """Flush all pending input from the buffer."""
    stdscr.nodelay(True)
    try:
        while stdscr.getch() != -1:
            pass
    finally:
        stdscr.nodelay(False)
        curses.flushinp()
```

**Call this before:**

- Any `ChoiceMenu.display()`
- Any `TimedPuzzle.display()`
- Any manual `getstr()` input

### 3.2 Logging System

**Create `engine/logger.py`:**

```python
import logging
import os

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/fotd.log"),
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger("fotd")
```

**Import and use throughout:**

```python
from engine.logger import logger

logger.info(f"Entering scene: {scene_id}")
logger.error(f"Puzzle failed: {target_word}")
```

### 3.3 Terminal Safety Wrapper

**Update main.py entry point:**

```python
def main_curses(stdscr):
    try:
        ensure_min_terminal(stdscr)
        run_game(stdscr)
    except KeyboardInterrupt:
        logger.info("User interrupted")
    except Exception as e:
        logger.exception("Fatal error")
        try:
            os.system("reset")
        except:
            pass
        print("Lattice crashed. Check logs/fotd.log")
```

**Add `ensure_min_terminal(stdscr)` helper using Phase 5.5.**

---

## 📋 Phase 4: Enhanced Mechanics

### 4.1 Corruption Effects on ChoiceMenu

**Update `engine/elements.py` ChoiceMenu:**

```python
def display(self, stdscr) -> int:
    # ... existing setup ...

    while True:
        # ... existing clear and render ...

        # CORRUPTION EFFECTS:
        if self.corruption >= 5 and self.selected_index == idx and random.random() < 0.2:
            # Glitchy arrow
            glitch_arrows = ["→ ", "» ", "▓ ", "█ ", "▒ "]
            prefix = random.choice(glitch_arrows)
        elif self.corruption >= 7 and random.random() < 0.1:
            # Shuffle options occasionally
            shuffled_choices = self.choices.copy()
            random.shuffle(shuffled_choices)
            # Use shuffled for display but preserve selection logic

        # ... rest of render loop
```

### 4.2 Stability Puzzle Bonus

**Update `TimedPuzzle` constructor:**

```python
def __init__(self, target_word: str, difficulty: int = 1, time_limit: float = 10.0, game_state=None):
    self.game_state = game_state
    bonus_time = game_state.stability // 4 if game_state else 0  # +2s at stability 8
    self.time_limit = time_limit + bonus_time
```

**Pass `game_state` when creating puzzles in scenes.**

### 4.3 Pause Menu

**Add to `engine/menu.py`:**

```python
class PauseMenu(ChoiceMenu):
    def __init__(self, game_state: GameState):
        stats = [
            f"Resume",
            f"Stability: {game_state.stability}/10",
            f"Corruption: {game_state.corruption_level}/10",
            f"Fragments: {len(game_state.identity_fragments)}",
            "Save Game",
            "Quit"
        ]
        super().__init__("PAUSED", stats, game_state.corruption_level)
```

**Wire ESC key to show pause menu in main loops.**

---

## 📋 Phase 5: Quick Wins & Polish

### 5.1 Skip Animation Hotkey

**Update `print_typing()` in `engine/console_effects.py`:**

```python
def print_typing(text, seconds_per_char=0.03, color=Colors.RESET, stdscr=None, ...):
    stdscr.nodelay(True)
    skip = False

    for idx, ch in enumerate(text):
        # Skip detection
        try:
            key = stdscr.getch()
            if key in [10, 13, 32, ord('s')]:  # Enter, Space, 's'
                skip = True
                break
        except:
            pass

        if not skip:
            # ... render char ...
            time.sleep(seconds_per_char)

    stdscr.nodelay(False)
```

### 5.2 Terminal Size Check

**engine/ui_utils.py:**

```python
def ensure_min_terminal(stdscr, min_height=30, min_width=100):
    h, w = stdscr.getmaxyx()
    if h < min_height or w < min_width:
        msg_lines = [
            f"Terminal too small: {w}x{h}",
            f"Minimum required: {min_width}x{min_height}",
            "Please resize and restart.",
            ""
        ]
        box = MessageBox(msg_lines, title="TERMINAL ERROR")
        box.display(stdscr)
        stdscr.getch()
        sys.exit(1)
```

### 5.3 Config System

**engine/config.py:**

```python
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
    def test(self):
        return self.data["debug"]["test_mode"]

    @property
    def skip_startup(self):
        return self.data["debug"]["skip_startup"]

    # Add getters for other values

config = Config()
```

### 5.4 End Screen Stats

**Create `engine/end_screen.py` and call after final scene:**

```python
def show_end_screen(stdscr, game_state: GameState, ending: str):
    stats = [
        f"Ending: {ending.upper()}",
        f"Final Stability: {game_state.stability}",
        f"Final Corruption: {game_state.corruption_level}",
        f"Fragments Collected: {len(game_state.identity_fragments)}",
        f"Puzzles Solved: {game_state.puzzles_solved}",
        f"Total Playtime: {game_state.playtime_seconds:.0f}s"
    ]

    box = MessageBox(stats, title=f"{ending.upper()} PROTOCOL", border_color=Colors.BOLD_MAGENTA)
    box.display(stdscr)
```

---

## 📋 Phase 6: Testing & Validation

### 6.1 Test Checklist

**Run these tests and document results in `TEST_RESULTS.md`:**

```
✅ New Game → Node 0x1 → Explore → Follow → Node 0x2 → Solve Puzzle → Save → Restart → Load → Resume
✅ New Game → Node 0x1 → Stand Still → Resist → Node 0x2 → Fail Puzzle → Check corruption increase
✅ Trigger corruption effects (set corruption=5 manually)
✅ Trigger stability bonus (set stability=6 manually)
✅ Resize terminal too small → proper error
✅ Spam keys during typing → no bleed to menus
✅ ESC → pause menu → resume
✅ Manual save/load via pause menu
✅ Check fotd.log for activity
✅ Check config.json loads correctly
```

### 6.2 Create Migration Script

**migrate_dialogue.py** – Semi-automate moving content from old `dialogue.py` to new scene files.

---

## 📋 Deliverables Checklist

```
✅ [Phase 1] README_REFACTOR.md with repo analysis
✅ [Phase 2] Enhanced GameState, scene architecture, save system
✅ [Phase 3] Input flushing, logging, error handling
✅ [Phase 4] Corruption/stability mechanics, pause menu
✅ [Phase 5] Skip hotkey, terminal check, config system, end screen
✅ [Phase 6] TEST_RESULTS.md with full test coverage
✅ Game runs end-to-end without crashes
✅ All existing content preserved (no content loss)
✅ New features work as specified
```

## 🎯 Success Criteria

1. **Game plays identically** to current version (same narrative flow).
2. **New systems work** (save/load, pause, config, stats).
3. **Scalable foundation** (easy to add Node 0x3).
4. **Production ready** (logging, error handling, graceful degradation).
5. **No regressions** (existing features all work).
