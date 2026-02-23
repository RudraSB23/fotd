# Fragments of the Lattice - Refactor Documentation

## Current File Structure

- `main.py`: Game entry point and top-level loops.
- `dialogue.py`: Contains narrative sequences and dialogue branching logic.
- `engine/`: Core modular components.
  - `state_manager.py`: `GameState` class.
  - `save_manager.py`: Persistence logic.
  - `elements.py`: UI elements like `ChoiceMenu`, `MessageBox`, `TimedPuzzle`.
  - `console_effects.py`: Text animations and colors.
  - `audio.py`: Sound and music management.
  - `menu.py`: Main and specialized menus.
- `assets/`: ASCII art and sound files.

## Key Classes & Responsibilities

- `GameState`: Tracks player stats (stability, corruption, fragments, relationships).
- `SaveManager`: Handles JSON serialization/deserialization of game state.
- `ChoiceMenu`: Interactive menus with keyboard navigation.
- `TimedPuzzle`: Leetspeak-based unscrambling puzzles.
- `AudioManager`: Pygame-based sound engine.

## Game Flow

1. `main.py` initializes curses and AudioManager.
2. Shows title screen (GrubMenu).
3. "New Game" or "Continue" logic resets or restores `GameState`.
4. Narrative flow starts with `onboarding` -> `initiating_sequence` -> `system_reboot`.
5. Enters main narrative scenes (e.g., `scene1_identity_sequence`).

## Assets Structure

- `assets/ascii/`: .txt files for terminal art.
- `assets/sounds/`: .mp3 and .wav files for themes and effects.
