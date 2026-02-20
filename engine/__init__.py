"""Engine package for Fragments of the Lattice.

Exposes core utilities used by the main game loop.
"""

from .console_effects import print_typing, print_colored, print_glitch, Colors
from .state_manager import GameState
from .assets import load_ascii_art

__all__ = [
    "print_typing",
    "print_colored",
    "print_glitch",
    "Colors",
    "GameState",
    "load_ascii_art",
]


