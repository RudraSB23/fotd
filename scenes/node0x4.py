import curses
import time
from engine.state_manager import GameState
from engine.save_manager import SaveManager
from engine.console_effects import print_typing, Colors, clear_terminal, print_glitch
from engine.elements import ChoiceMenu
from engine.audio import AudioManager
from .base_scene import BaseScene

audio = AudioManager()

class Scene4Elias(BaseScene):
    def run(self, stdscr, game_state: GameState) -> str:
        SaveManager.save_game(game_state, "node0x4_elias", stdscr)
        
        clear_terminal(stdscr)
        print_typing("<<< ENTERING NODE 0x4: FRAGMENT BETA >>>", 0.05, Colors.BOLD_GREEN, stdscr)
        time.sleep(1)
        
        print_typing("\nThe geometry surrounding you warps into a decaying server room.", 0.03, Colors.WHITE, stdscr)
        print_typing("Sparks shower from overhead conduits as a cynical figure materializes.", 0.03, Colors.CYAN, stdscr)
        time.sleep(1)
        
        print_typing('\n"You\'re still trying to fix the leaks?"', 0.04, Colors.YELLOW, stdscr)
        print_typing('"The ship sank decades ago, Architect."', 0.04, Colors.YELLOW, stdscr)
        time.sleep(1)
        
        print_typing("\nIt's Elias. Or a fragment of the entity that used to be him.", 0.03, Colors.WHITE, stdscr)
        print_typing("His code is slowly weeping into the floor, an agonizing loop of self-awareness.", 0.03, Colors.WHITE, stdscr)
        time.sleep(1)
        
        menu = ChoiceMenu(
            "What do you do with his fragment?",
            [
                "Restore Elias (Impose painful memory for stability)",
                "Delete Elias (Grant oblivion as mercy)"
            ]
        )
        choice = menu.display(stdscr)
        
        clear_terminal(stdscr)
        if choice == 0:
            # Restore Elias
            print_typing("\nYou inject stabilizing routines into Elias's matrix.", 0.03, Colors.CYAN, stdscr)
            time.sleep(1)
            audio.play_sound("beep.mp3")
            print_typing('\n"No... please! I don\'t want to remember the fire! Don\'t make me hold this!"', 0.05, Colors.YELLOW, stdscr)
            time.sleep(1)
            print_typing("\nHis shape solidifies, trapped once more in the agony of existence.", 0.04, Colors.WHITE, stdscr)
            
            game_state.apply_effect("stability+2")
            game_state.apply_effect("corruption-1")
            game_state.npc_relationships["elias"] = "restored"
            
        else:
            # Delete Elias
            print_typing("\nYou bypass the stabilizing routines, allowing his code to bleed out.", 0.04, Colors.RED, stdscr)
            time.sleep(1)
            audio.play_sound("beep.mp3")
            print_typing('\n"Thank you... into the dark we go..."', 0.05, Colors.YELLOW, stdscr)
            time.sleep(1)
            print_typing("\nElias dissolves completely, leaving nothing but an empty silence.", 0.04, Colors.WHITE, stdscr)
            
            game_state.apply_effect("corruption+2")
            game_state.apply_effect("stability-1")
            game_state.npc_relationships["elias"] = "deleted"

        time.sleep(2)
        return "node0x7_lyra"
