import curses
import time
import sys
from engine.core.state_manager import GameState
from engine.core.save_manager import SaveManager
import engine.core.config
from engine.ui.console_effects import print_typing, Colors, clear_terminal, print_glitch
from .intro_sequence import fake_error_flood
from engine.ui.elements import ChoiceMenu, MessageBox, TimedPuzzle
from engine.ui.end_screen import EndScreen
from engine.core.audio import AudioManager
from .base_scene import BaseScene

audio = AudioManager()

class Scene9Ending(BaseScene):
    def run(self, stdscr, game_state: GameState, getch_func=None) -> str:
        SaveManager.save_game(game_state, "node0x9_ending", stdscr)
        
        clear_terminal(stdscr)
        print_typing("<<< ENTERING NODE 0x9: THE THRESHOLD >>>", 0.05, Colors.BOLD_GREEN, stdscr=stdscr, getch_func=getch_func)
        time.sleep(1)
        
        print_typing("\nThe Lattice narrows into a searing, singular corridor of white light.", 0.03, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
        
        # Elias puzzle logic
        if game_state.npc_relationships.get("elias") == "deleted":
            print_typing("The void interference of deleted fragments tears at the pathway!", 0.04, Colors.RED, stdscr=stdscr, getch_func=getch_func)
            time.sleep(1)
            audio.play_sound("scary_static.mp3", loop=False)
            print_typing("[SYSTEM]: PRESS [ENTER] TO STABILIZE INCOMING CORRUPTION", 0.03, Colors.BOLD_RED, stdscr=stdscr, getch_func=getch_func)
            while True:
                getch = getch_func or stdscr.getch
                key = getch()
                if key == -999: return None # Handle quit
                if key in [10, 13]: break
            
            puzzle = TimedPuzzle("OBLIVION", difficulty=3, time_limit=8.0)
            if not puzzle.display(stdscr, getch_func=getch_func):
                print_typing("The void pulls you down...", 0.05, Colors.RED, stdscr=stdscr, getch_func=getch_func)
                game_state.apply_effect("corruption+3")
            else:
                print_typing("You rip your way through the interference...", 0.04, Colors.GREEN, stdscr=stdscr, getch_func=getch_func)
                
        elif game_state.npc_relationships.get("elias") == "restored":
            print_typing("A ghostly figure appears in the data-stream, stabilizing your connection.", 0.04, Colors.CYAN, stdscr=stdscr, getch_func=getch_func)
            print_typing('"I am in agony... but I will hold the door for you." - Elias', 0.05, Colors.YELLOW, stdscr=stdscr, getch_func=getch_func)
            time.sleep(1)
            game_state.apply_effect("stability+2")
            
        time.sleep(1)
        clear_terminal(stdscr)
        
        # Identity Mirror logic
        if "IdentityMirror" in game_state.identity_fragments:
            print_typing("\nYou approach the Identity Mirror...", 0.04, Colors.BOLD_WHITE, stdscr=stdscr, getch_func=getch_func)
            time.sleep(1)
            print_typing("For the first time, a mirror image appears.", 0.04, Colors.CYAN, stdscr=stdscr, getch_func=getch_func)
            print_typing("But its mouth moves independently of your own.", 0.05, Colors.RED, stdscr=stdscr, getch_func=getch_func)
        else:
            print_typing("\nYou reach the terminal core.", 0.04, Colors.BOLD_WHITE, stdscr=stdscr, getch_func=getch_func)
            time.sleep(1)
            print_typing("A shadow detaches itself from the walls of the chamber.", 0.04, Colors.RED, stdscr=stdscr, getch_func=getch_func)
            
        time.sleep(2)
        print_typing('\nThe Echo fully manifests in front of you.', 0.05, Colors.BOLD_MAGENTA, stdscr=stdscr, getch_func=getch_func)
        time.sleep(1)
        
        ending = game_state.get_ending()
        
        if ending == "restoration":
            # Restoration Protocol (Stability >= 8)
            print_typing('\n"The Lattice is clean," the Echo murmurs.', 0.06, Colors.MAGENTA, stdscr=stdscr, getch_func=getch_func)
            print_typing('"The memories are safe. But there is no room for a ghost like you."', 0.06, Colors.MAGENTA, stdscr=stdscr, getch_func=getch_func)
            time.sleep(3)
            
            clear_terminal(stdscr)
            print_typing("Your vision dissolves. Data compiles perfectly behind you.", 0.04, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
            print_typing("You fade into the loading dots. Slowly. Forever.", 0.05, Colors.WHITE, stdscr=stdscr, getch_func=getch_func)
            time.sleep(2)
            EndScreen().display(stdscr, game_state)
            
        elif ending == "collapse":
            # Collapse (Corruption >= 8)
            print_typing('\n"Finally," the Echo laughs.', 0.06, Colors.MAGENTA, stdscr=stdscr, getch_func=getch_func)
            print_typing('"The loop breaks. The code bleeds out. Let there be nothing."', 0.06, Colors.BOLD_RED, stdscr=stdscr, getch_func=getch_func)
            time.sleep(3)
            
            audio.play_sound("scary_static.mp3", loop=True)
            fake_error_flood(stdscr, 30)
            audio.stop_sound("scary_static.mp3")
            
            clear_terminal(stdscr)
            stdscr.bkgd(' ', curses.color_pair(Colors.BOLD_WHITE))
            stdscr.refresh()
            time.sleep(1)
            # Revert background to black so we actually see the red text
            stdscr.bkgd(' ', curses.color_pair(Colors.WHITE))
            print_typing("SYSTEM MELTDOWN COMPLETED", 0.02, Colors.RED, stdscr=stdscr, getch_func=getch_func)
            time.sleep(2)
            EndScreen().display(stdscr, game_state)
            
        else:
            # Integration (Balanced State)
            print_typing('\n"We are the archive," the Echo whispers, blending with your thoughts.', 0.06, Colors.MAGENTA, stdscr=stdscr, getch_func=getch_func)
            print_typing('"We are the architects of our own haunting. Let us continue."', 0.06, Colors.BOLD_MAGENTA, stdscr=stdscr, getch_func=getch_func)
            time.sleep(3)
            
            clear_terminal(stdscr)
            # Screen turns magenta effect
            if not engine.core.config.config.SKIP_ANIMATIONS:
                for _ in range(3):
                    stdscr.bkgd(' ', curses.color_pair(Colors.MAGENTA))
                    stdscr.refresh()
                    time.sleep(0.3)
                    stdscr.bkgd(' ', curses.color_pair(Colors.WHITE))
                    stdscr.refresh()
                    time.sleep(0.3)
                
            print_typing("THE LOOP BEGINS ANEW", 0.05, Colors.BOLD_WHITE, stdscr=stdscr, getch_func=getch_func)
            time.sleep(2)
            
            # Restart setup logic
            game_state.player_name = "The Echo"
            game_state.stability = 3
            game_state.corruption_level = 0
            game_state.identity_fragments.clear()
            game_state.puzzles_solved = 0
            game_state.puzzles_failed = 0
            game_state.npc_relationships.clear()
            
            # Meta loop restart
            return "scene1_identity_sequence"
            
        return None
