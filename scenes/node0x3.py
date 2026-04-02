import curses
import time
from engine.core.state_manager import GameState
from engine.core.save_manager import SaveManager
from engine.ui.console_effects import print_typing, Colors, clear_terminal, print_glitch
from engine.ui.elements import ChoiceMenu, MessageBox, TimedPuzzle
from engine.core.audio import AudioManager
from .base_scene import BaseScene

audio = AudioManager()

class Scene3Archive(BaseScene):
    def run(self, stdscr, game_state: GameState, getch_func=None) -> str:
        SaveManager.save_game(game_state, "node0x3_archive", stdscr)
        
        clear_terminal(stdscr)
        print_typing("<<< ENTERING NODE 0x3: THE ARCHIVE >>>", 0.05, Colors.BOLD_GREEN, stdscr=stdscr, getch_func=getch_func)
        time.sleep(1)
        
        print_typing("\nThe small room pulses, its boundaries dissolving into a vast, stretching architecture.", 0.03, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
        print_typing("You stand inside a sprawling library of glowing data cubes, stacked endlessly into the zenith.", 0.03, Colors.CYAN, stdscr=stdscr, getch_func=getch_func)
        audio.play_sound("beep.mp3")
        time.sleep(1)
        
        while True:
            clear_terminal(stdscr)
            print_typing("ARCHIVE ACCESS TERMINAL", 0.02, Colors.BOLD_WHITE, stdscr=stdscr, getch_func=getch_func)
            print_typing("Multiple data cubes hum with residual energy. What do you investigate?", 0.02, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
            
            menu = ChoiceMenu(
                "Select a cube to decrypt:",
                [
                    "Cube Alpha (Public Logs)",
                    "Cube Sigma (Encrypted)",
                    "Proceed deeper into the Lattice"
                ]
            )
            choice = menu.display(stdscr, getch_func=getch_func)
            if choice == -999: return -999
            
            if choice == 0:
                result = self.cube_alpha(stdscr, getch_func=getch_func)
                if result == -999: return -999
            elif choice == 1:
                result = self.cube_sigma(stdscr, game_state, getch_func=getch_func)
                if result == -999: return -999
            elif choice == 2:
                break
                
        # The Echo's perspective
        clear_terminal(stdscr)
        print_typing("\nThe Echo speaks, its voice resonating not from the walls, but inside your head.", 0.04, Colors.MAGENTA, stdscr=stdscr, getch_func=getch_func)
        print_typing('"Why restore a memory of a world that burned? Let them sleep in the static."', 0.06, Colors.MAGENTA, stdscr=stdscr, getch_func=getch_func)
        time.sleep(2)
        
        return "node0x4_elias"

    def cube_alpha(self, stdscr, getch_func=None):
        getch = getch_func or stdscr.getch
        clear_terminal(stdscr)
        msg = [
            ("PUBLIC LOG [RECORD 40X]:", Colors.BOLD_CYAN),
            "",
            "The world above is ending. The skies burn with a fire",
            "that the atmosphere cannot extinguish.",
            "The Architect proposed the Lattice. A sanctuary for thought,",
            "where flesh could be discarded to preserve the mind."
        ]
        MessageBox(msg, title="CUBE ALPHA DECRYPTED", border_color=Colors.CYAN).display(stdscr, duration=4)
        print_typing("\nPress any key to step back...", 0.01, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
        
        stdscr.nodelay(False)
        while True:
            key = getch()
            if key == -999: return -999
            if key != -1: break
        stdscr.nodelay(True)
        return 0

    def cube_sigma(self, stdscr, game_state, getch_func=None):
        getch = getch_func or stdscr.getch
        clear_terminal(stdscr)
        print_typing("This cube is heavily encrypted. A fracture barrier blocks access.", 0.03, Colors.RED, stdscr=stdscr, getch_func=getch_func)
        time.sleep(1)
        print_typing("[SYSTEM]: PRESS [ENTER] TO INITIATE DECRYPTION BYPASS", 0.03, Colors.BOLD_RED, stdscr=stdscr, getch_func=getch_func)
        
        stdscr.nodelay(False)
        while True:
            key = getch()
            if key == -999: return -999
            if key in [10, 13]:
                break
        stdscr.nodelay(True)
                
        # Puzzle
        puzzle = TimedPuzzle("SHATTERED", difficulty=2, time_limit=12.0 + (game_state.stability // 3))
        success = puzzle.display(stdscr, getch_func=getch_func)
        
        clear_terminal(stdscr)
        if success:
            game_state.puzzles_solved += 1
            game_state.apply_effect("stability+1")
            
            # Additional Lore
            msg = [
                ("ENCRYPTED LOG [ARCHITECT SECRETS]:", Colors.BOLD_MAGENTA),
                "",
                "To save them, I had to shatter them.",
                "Human minds could not survive the transfer intact.",
                "I broke their identities into fragments.",
                "It was the only way to save humanity from the End.",
                "Will they ever forgive me?"
            ]
            MessageBox(msg, title="CUBE SIGMA DECRYPTED", border_color=Colors.MAGENTA).display(stdscr, duration=5)
        else:
            game_state.puzzles_failed += 1
            game_state.apply_effect("corruption+1")
            print_typing("The cube bursts into static. The data is lost to the void.", 0.03, Colors.BOLD_RED, stdscr=stdscr, getch_func=getch_func)
            print_typing('"Some things are better left buried..."', 0.05, Colors.MAGENTA, stdscr=stdscr, getch_func=getch_func)
            
        print_typing("\nPress any key to step back...", 0.01, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
        
        stdscr.nodelay(False)
        while True:
            key = getch()
            if key == -999: return -999
            if key != -1: break
        stdscr.nodelay(True)
        return 0
