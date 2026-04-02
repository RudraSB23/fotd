"""Engine package for Fragments of the Lattice.

Exposes core utilities used by the main game loop.
"""

from .ui.console_effects import print_typing, print_colored, print_glitch, Colors, get_curses_color
from .core.state_manager import GameState
from .core.assets import load_ascii_art
from .core.config import config
from .core.logger import game_logger

__all__ = [
    "print_typing",
    "print_colored",
    "print_glitch",
    "Colors",
    "get_curses_color",
    "GameState",
    "load_ascii_art",
    "config",
    "game_logger",
]


