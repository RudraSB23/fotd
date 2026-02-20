# Project Analysis: Fragments of the Lattice

This document provides a technical and narrative breakdown of the "Fragments of the Lattice" project. It serves as an all-in-one reference for understanding, maintaining, and expanding the game.

## 1. Project Overview

**Fragments of the Lattice** (referred to in some logs as _Asylum Shadows_) is a terminal-based narrative horror game. Players take on the role of the "Caretaker" (or Architect), exploring a crumbling digital archive of human memories known as "The Lattice." The gameplay combines ASCII art, glitch aesthetics, and choice-based branching.

**Core Mechanics:**

- **State Management:** Tracking "Stability" (order/repair) vs. "Corruption" (chaos/Echo influence).
- **Glitch Aesthetic:** Real-time text distortion and terminal-level visual effects.
- **Narrative Depth:** Branching paths influenced by player choices and stat thresholds.
- **Hardware Integration:** Experimental "Echo Watch" feature that uses a webcam to capture ASCII "reflections" of the player.

---

## 2. Directory Tree

```
C:\Users\Rudra Singh Bhardwaj\Desktop\fotd\1.3\
├── main.py                 # Entry point & game loop
├── dialogue.py             # Narrative sequences & UI logic
├── TEST.py                 # "Echo Watch" camera-to-ASCII utility
├── lore.md                 # Background & world-building
├── INTERACTIONS.md         # Game flow & mechanics roadmap
├── game_overview.md        # Comprehensive summary document
├── fixes.md                # Maintenance & architectural suggestions
├── LATEST FIXES.txt        # Recent development notes
├── assets/                 # Game assets
│   ├── ascii_art/          # Narrative & UI ASCII art
│   ├── images/             # Logos and static images
│   └── sounds/             # Music & SFX (mp3/wav)
└── engine/                 # Modular game engine
    ├── __init__.py         # Package interface
    ├── assets.py           # Resource loading utilities
    ├── audio.py            # Sound & music management
    ├── console_effects.py  # Glitch, color, and typing effects
    ├── elements.py         # Choice-based menu components
    ├── menu.py             # Main interactive menu (GrubMenu)
    └── state_manager.py    # Global game state persistence
```

---

## 3. File-by-File Breakdown

### Root Files

#### `main.py`

- **Role:** The orchestrator of the game. Handles initialization, the main menu, and transitions into game scenes.
- **Important Code:**
  - `run_game(stdscr)`: The core sequence that boots the engine, loads the title art, and kicks off `scene1_identity_sequence`.
  - `GrubMenu` integration: Manages the initial "Continue/New Game" choice with glitch animations.
- **Notable Logic:** Uses `curses.wrapper` to ensure terminal settings are restored if the game crashes.

#### `dialogue.py`

- **Role:** Contains all narrative strings, sequence logic, and specialized UI effects like "stability bars."
- **Important Functions:**
  - `intro_systems_rebooting_bar()`: An animated loading bar using curses.
  - `corruption_flash()`: A high-intensity visual glitch sequence.
  - `scene1_identity_sequence()`: The first narrative branch where the player registers their identity.
  - `echo_line()`: A specialized "scary" typing function that randomly corrupts characters using a lookup table.
- **Key Variables:** `SYSTEM_MESSAGES`, `INITIATION_ECHO_MESSAGES`, `ECHO_LINES_SCENE1` (pools of flavor text used to create atmosphere).

#### `TEST.py`

- **Role:** An experimental utility for camera interaction ("Echo Watch").
- **Important Functions:**
  - `frame_to_ascii()`: Uses OpenCV to process webcam frames into Grayscale, then maps pixel intensity to a custom UTF-8 character ramp (`█▓▒░...`).
  - `echo_watch_event()`: Captures a photo, prints it to the terminal, and saves it to a `LATTICE_SEES_YOU` folder on the desktop.
- **Dependencies:** `cv2` (OpenCV), `numpy`.

---

### Engine Module (`/engine`)

#### `state_manager.py`

- **Role:** Manages the data-driven soul of the game.
- **Classes:**
  - `GameState`: A dataclass storing `player_name`, `corruption_level`, `stability`, `identity_fragments`, and `npc_relationships`.
  - `apply_effect(effect_str)`: Parses string commands (e.g., `"stability+1"`) to mutate state.
  - `ending()`: Logic to determine which ending is triggered based on final stats.

#### `console_effects.py`

- **Role:** The "GPU" of the game. Handles all specialized rendering.
- **Key Constants:** `CORRUPTION_MAP` (maps 'a' to '@', 'e' to '3', etc. for glitch effects).
- **Functions:**
  - `print_typing()`: Progressive text reveal with integrated sound effects.
  - `print_glitch()`: Temporarily scrambles characters to simulate terminal corruption.
  - `CursesColors`: Maps ANSI escape codes to `curses` color pairs for cross-platform compatibility.

#### `audio.py`

- **Role:** Audio middleware.
- **Classes:**
  - `AudioManager`: Wraps `pygame.mixer`. Preloads all files from `/assets/sounds` automatically.
- **Logic:** Handles background music (looping) and one-shot sound effects separately.

#### `menu.py` & `elements.py`

- **Role:** Interaction components.
- **Classes:**
  - `GrubMenu`: A fullscreen menu with synchronized visual/audio glitch pulses during idle time.
  - `ChoiceMenu`: A more compact menu used for in-dialogue decisions.

---

### Documentation & Narrative Files

#### `lore.md`

- **Purpose:** Deep background on "The Lattice," the "Architect," and the "Echo."
- **Key Insight:** Reveals that the player is effectively debugging their own mind; the "Echo" is the part of the player that wants to let go.

#### `INTERACTIONS.md`

- **Purpose:** Technical roadmap.
- **Key Details:** Defines the specific stat thresholds (e.g., `corruption >= 8` triggers "Forced Glitch Mode") and maps out the 9 planned "Nodes" of the game.

#### `fixes.md` & `LATEST FIXES.txt`

- **Purpose:** Tracks bugs (e.g., dialogue overlapping over old text) and architectural debt (e.g., code duplication between `corruption_flash` and `TitleAnimator`).

---

## 4. Cross-File Connections

- **State Flow:** `main.py` initializes `GameState`, which is then passed to `scene` functions in `dialogue.py`. These functions call `game_state.apply_effect()` to store player choices.
- **Resource Pipeline:** `engine/assets.py` provides the `load_ascii_art` tool used by almost every root file to pull from `assets/ascii_art/`.
- **Global Settings:** `engine/audio.py` attempts to import `ENABLE_SOUNDS` and `ENABLE_MUSIC` from `main.py`, creating a loose but important coupling for settings management.

---

## 5. Suggestions for Improvement

1. **Unify Rendering Logic:** Merge `corruption_flash` (dialogue.py) with the idle glitch logic in `GrubMenu` (menu.py) into a central `GlitchEngine` class.
2. **Abstract Choices:** Move dialogue text and choices into a JSON or YAML file to separate narrative from Python logic, making it easier to add new nodes.
3. **Robust Input Handling:** The current `stdscr.getch()` approach in some menus may not handle window resizing or edge-case keyboard inputs gracefully.
4. **Echo Watch Integration:** Fully integrate `TEST.py` logic into `dialogue.py` during "Mirror" or "Meta" sequences to create a seamless horror moment.
5. **Config System:** Replace the `try/import` hack in `audio.py` with a proper `config.py` or `.env` loader.
