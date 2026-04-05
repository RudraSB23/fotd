import curses
import time
from engine.core.state_manager import GameState
from engine.core.save_manager import SaveManager
from engine.ui.console_effects import print_typing, Colors, clear_terminal
from .base_scene import BaseScene

class Scene3Archive(BaseScene):
    def run(self, stdscr, game_state: GameState, getch_func=None) -> str:
        SaveManager.save_game(game_state, "node0x3_archive", stdscr)
        
        from engine.ui.console_effects import full_screen_glitch, print_centered
        
        # 1. Glitch transition
        full_screen_glitch(stdscr, frames=10, frame_delay=0.02)
        clear_terminal(stdscr)
        audio.play_sound("beep.mp3")
        
        # 2. Centered High-Impact Header
        stdscr.attron(curses.A_BOLD)
        print_centered("<<< ENTERING NODE 0x3: THE ARCHIVE >>>", color=Colors.BOLD_GREEN, stdscr=stdscr)
        stdscr.attroff(curses.A_BOLD)
        
        time.sleep(2.0)
        
        return "node0x4_elias"
