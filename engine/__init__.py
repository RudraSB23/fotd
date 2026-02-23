"""Engine package for Fragments of the Lattice.

Exposes core utilities used by the main game loop.
"""

from .console_effects import print_typing, print_colored, print_glitch, Colors, get_curses_color
from .state_manager import GameState
from .assets import load_ascii_art
from .config import config

__all__ = [
    "print_typing",
    "print_colored",
    "print_glitch",
    "Colors",
    "get_curses_color",
    "GameState",
    "load_ascii_art",
    "config",
]


