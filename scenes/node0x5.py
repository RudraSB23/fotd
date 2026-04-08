import curses
import time

from engine.core.audio import AudioManager
from engine.core.save_manager import SaveManager
from engine.core.state_manager import GameState
from engine.ui.console_effects import (
    Colors,
    clear_terminal,
    print_centered,
    print_glitch,
    print_typing,
)

from .base_scene import BaseScene

audio = AudioManager()


class Scene5Experimental(BaseScene):
    def run(self, stdscr, game_state: GameState, getch_func=None) -> str:
        SaveManager.save_game(game_state, "node0x5_experimental", stdscr)

        clear_terminal(stdscr)
        audio.play_sound("beep.mp3")

        for i in range(20):
            print_glitch(
                "<<< ENTERING NODE 0x5: EXPERIMENTAL VOID >>>",
                base_color=Colors.BOLD_GREEN,
                glitch_color=True,
                stdscr=stdscr,
                getch_func=getch_func,
                center=True,
                intensity=1 - (i * 0.05),
            )
            time.sleep(0.05)
        clear_terminal(stdscr)
        print_centered(
            "<<< ENTERING NODE 0x5: EXPERIMENTAL VOID >>>",
            color=Colors.BOLD_GREEN,
            stdscr=stdscr,
            offset=-1,
        )
        time.sleep(1.0)
        clear_terminal(stdscr)
        time.sleep(1.0)

        return "node0x6_synch"
