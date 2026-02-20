import os
import getpass
import time
import curses

from pygame.time import delay

from engine import config
from engine.assets import load_ascii_art, load_multiple_ascii_art
from engine.console_effects import print_colored, print_typing, clear_terminal, Colors, print_centered
from engine.elements import ChoiceMenu, MessageBox
from engine.save_manager import SaveManager
from engine.state_manager import *
from engine.audio import AudioManager
from engine.menu import GrubMenu
from dialogue import *

audio = AudioManager()


def run_game(stdscr):
    # setup curses screen
    curses.curs_set(0)
    stdscr.nodelay(False)
    clear_terminal(stdscr)

    # Wait for assets to finish preloading if they aren't done yet
    if not audio.is_loading_finished():
        audio.wait_for_assets()
    
    game_state = GameState()
    time.sleep(0.5)

    # Debug Bypass
    if config.TEST:
        game_state.player_name = "TEST"
        import dialogue
        
        # Dynamically look up the function in the dialogue module
        scene_func = getattr(dialogue, str(config.TEST), None)
        
        if scene_func and callable(scene_func):
            # Modular MessageBox for bypass notification
            msg = [
                "",
                ("TEST MODE STORY BYPASS", Colors.BOLD_RED),
                "",
                ("Continuing from:", Colors.BOLD_WHITE),
                (f"[{config.TEST}]", Colors.BOLD_WHITE)
            ]
            box = MessageBox(msg, title="ADMIN OVERRIDE", border_color=Colors.BOLD_MAGENTA)
            box.display(stdscr, duration=3.0)
            time.sleep(1)
            if config.TEST == 'system_reboot':
                player_name = system_reboot(stdscr, game_state)
            else:
                scene_func(stdscr, game_state)
            return
        else:
            print_colored(f"\n[DEBUG ERROR] Scene '{config.TEST}' not found in dialogue.py!", Colors.BOLD_RED, stdscr=stdscr)
            time.sleep(2)

    while True:
        # load title
        title = load_ascii_art("title.txt")
        audio.play_music("theme.mp3", loop=True, volume=0.5)
        time.sleep(0.5)

        if title:
            menu = GrubMenu(
                ["Continue", "New Game"],
                title=title,
                title_menu_spacing=5,
                vertical_offset=2,
                glitchify=True,
            )
            choice_index = menu.display(stdscr)
        else:
            print_typing("FRAGMENTS OF THE LATTICE", 0.03, Colors.GREEN, stdscr=stdscr)
            menu = GrubMenu(["Continue", "New Game"], title=None)
            choice_index = menu.display(stdscr)

        audio.stop_music()
        clear_terminal(stdscr)
        
        if choice_index == 0: # Continue
            # Simulation/Loading of save data
            msg = [("SEARCHING FOR LOCAL FRAGMENTS...", Colors.BOLD_CYAN)]
            box = MessageBox(msg, title="SYSTEM SCAN", border_color=Colors.BOLD_CYAN)
            box.display(stdscr, duration=2.0)
            
            save_data = SaveManager.load_game()
            if save_data:
                game_state = SaveManager.restore_state(save_data)
                scene_name = save_data.get("current_scene")
                
                import dialogue
                scene_func = getattr(dialogue, str(scene_name), None)
                
                if scene_func and callable(scene_func):
                    # Success
                    success_msg = [
                        ("FRAGMENT RESTORED", Colors.BOLD_GREEN),
                        "",
                        f"Subject: {game_state.player_name}",
                        f"Location: {scene_name}",
                        "",
                        ("Re-aligning consciousness...", Colors.BOLD_WHITE)
                    ]
                    box = MessageBox(success_msg, title="SYNC SUCCESS", border_color=Colors.BOLD_GREEN)
                    box.display(stdscr, duration=2.0)
                    
                    # Start the game from the saved scene
                    scene_func(stdscr, game_state)
                    return
                else:
                    error_msg = [
                        ("LINK CORRUPTION", Colors.BOLD_RED),
                        "",
                        f"Could not resolve scene: {scene_name}",
                        "Data is unreadable.",
                        "",
                        ("Returning to primary node...", Colors.BOLD_WHITE)
                    ]
                    box = MessageBox(error_msg, title="NODE FAILURE", border_color=Colors.BOLD_RED)
                    box.display(stdscr)
            else:
                error_msg = [
                    ("CRITICAL ERROR", Colors.BOLD_RED),
                    "",
                    "No encrypted save data detected.",
                    "Local buffer is empty.",
                    "",
                    ("Returning to primary node...", Colors.BOLD_WHITE)
                ]
                error_box = MessageBox(error_msg, title="NODE FAILURE", border_color=Colors.BOLD_RED)
                error_box.display(stdscr)
            
            clear_terminal(stdscr)
            continue # Loop back to menu
            
        elif choice_index == 1: # New Game
            confirm_msg = [
                "This will overwrite any volatile data.",
                "",
                ("INITIATE NEURAL LINK?", Colors.BOLD_MAGENTA)
            ]
            confirm_box = MessageBox(confirm_msg, title="LINK ESTABLISHMENT", 
                                     choices=["Continue", "Cancel"],
                                     border_color=Colors.BOLD_MAGENTA)
            confirm_choice = confirm_box.display(stdscr)
            
            if confirm_choice == 0: # Continue
                SaveManager.delete_save() # Clear old data
                game_state = GameState() # Reset local state
                break # Break loop and start game
            else:
                clear_terminal(stdscr)
                continue # Loop back to menu

    time.sleep(1)
    onboarding(stdscr)
    time.sleep(1)
    initiating_sequence(stdscr)
    fake_error_flood(stdscr, random.randint(40,50))
    clear_terminal(stdscr)
    display_success_message(stdscr)
    memory_load_prompt(stdscr)

    corrupt_ascii = []
    for i in range(1,4):
        corrupt_ascii.append(load_ascii_art(f"intro_glitch_{i}.txt"))
    corruption_flash(stdscr, corrupt_ascii)

    time.sleep(2)
    if config.TEST and config.TEST != 'system_reboot':
        player_name = 'TEST'
    else:
        player_name = system_reboot(stdscr, game_state)
    
    game_state.player_name = player_name

    # start scene
    scene1_identity_sequence(stdscr, game_state)

    clear_terminal(stdscr)
    print_centered("[ TO BE CONTINUED... ]", Colors.BOLD_MAGENTA, stdscr=stdscr)
    time.sleep(3)



def main_curses(stdscr):
    while True:
        try:
            run_game(stdscr)
            break
        except KeyboardInterrupt:
            from engine.ui_utils import confirm_quit_menu
            if confirm_quit_menu(stdscr):
                import sys
                sys.exit(0)
            # If they cancel, we just continue the loop. 
            # Note: This will restart the title screen loop.
            from engine.console_effects import clear_terminal
            clear_terminal(stdscr)


if __name__ == "__main__":
    if config.TEST:
        config.SKIP_STARTUP = True
    if not config.SKIP_STARTUP:
        startup_screen(15)
        time.sleep(2)
    curses.wrapper(main_curses)
