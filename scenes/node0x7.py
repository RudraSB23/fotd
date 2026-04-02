import curses
import time
from engine.core.state_manager import GameState
from engine.core.save_manager import SaveManager
from engine.ui.console_effects import print_typing, Colors, clear_terminal, print_glitch
from engine.ui.elements import ChoiceMenu
from engine.core.audio import AudioManager
from .base_scene import BaseScene

audio = AudioManager()

class Scene7Lyra(BaseScene):
    def run(self, stdscr, game_state: GameState, getch_func=None) -> str:
        SaveManager.save_game(game_state, "node0x7_lyra", stdscr)
        
        clear_terminal(stdscr)
        print_typing("<<< ENTERING NODE 0x7: FRAGMENT GAMMA >>>", 0.05, Colors.BOLD_GREEN, stdscr=stdscr, getch_func=getch_func)
        time.sleep(1)
        
        print_typing("\nThe environment shifts into a panopticon—an endless array of tracking screens.", 0.03, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
        print_typing("A serene figure named Lyra is watching one of them. She turns to face you.", 0.03, Colors.CYAN, stdscr=stdscr, getch_func=getch_func)
        time.sleep(1)
        
        print_typing('\n"I\'ve watched you loop these nodes a thousand times."', 0.04, Colors.BLUE, stdscr=stdscr, getch_func=getch_func)
        print_typing('"Every time, you think you\'re choosing. Every time, you\'re just executing."', 0.05, Colors.BLUE, stdscr=stdscr, getch_func=getch_func)
        time.sleep(1)

        menu = ChoiceMenu(
            "How do you respond?",
            [
                "Challenge her nihilism (Claim your agency)",
                "Accept it (Acknowledge the cycle)"
            ],
            game_state.corruption_level
        )
        choice = menu.display(stdscr, getch_func=getch_func)
        
        clear_terminal(stdscr)
        if choice == 0:
            print_typing('\n"I choose because I must. I am the Caretaker, not a script."', 0.04, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
            time.sleep(1)
            print_typing('\nLyra smiles sadly. "A beautiful illusion. But illusions break under pressure."', 0.04, Colors.BLUE, stdscr=stdscr, getch_func=getch_func)
            game_state.apply_effect("stability+1")
            game_state.apply_effect("corruption-1")
        else:
            print_typing('\n"Perhaps you are right. We are all just compiling to the same end."', 0.04, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
            time.sleep(1)
            print_typing('\nLyra nods. "There is peace in knowing the train cannot leave the tracks."', 0.04, Colors.BLUE, stdscr=stdscr, getch_func=getch_func)
            game_state.apply_effect("corruption+1")
            game_state.apply_effect("stability-1")
            
        time.sleep(2)
        
        if game_state.stability > 7:
            clear_terminal(stdscr)
            audio.play_sound("beep.mp3")
            print_typing("\nLyra leans in closer, studying the unnatural cohesion of your form.", 0.04, Colors.CYAN, stdscr=stdscr, getch_func=getch_func)
            print_typing('\n"You are surprisingly whole... more stable than you should be."', 0.05, Colors.BLUE, stdscr=stdscr, getch_func=getch_func)
            time.sleep(1)
            print_typing('"If you truly wish to face the Architect of this cycle..."', 0.04, Colors.BLUE, stdscr=stdscr, getch_func=getch_func)
            print_typing('"Seek the Identity Mirror at the Threshold. It will reveal what you must do."', 0.06, Colors.BOLD_BLUE, stdscr=stdscr, getch_func=getch_func)
            game_state.add_fragment("IdentityMirror")
            time.sleep(3)

        return "node0x9_ending"
