import curses
import getpass
import os
import random
import time

from engine.core.assets import load_ascii_art, load_multiple_ascii_art
from engine.core.audio import AudioManager
from engine.core.config import config
from engine.core.save_manager import SaveManager
from engine.core.state_manager import GameState
from engine.ui.console_effects import (
    Colors,
    clear_terminal,
    print_centered,
    print_colored,
    print_typing,
)
from engine.ui.elements import ChoiceMenu, MessageBox
from engine.ui.menu import GrubMenu
from scenes.intro_sequence import (
    corruption_flash,
    display_success_message,
    initiating_sequence,
    loading_bar,
    memory_load_prompt,
    onboarding,
    system_reboot,
)
from scenes.registry import get_scene

audio = AudioManager()


def handle_interrupt(stdscr):
    from engine.ui.console_effects import Colors, clear_terminal
    from engine.ui.elements import MessageBox

    msg = [
        ("WARNING: SYSTEM INTERRUPTION DETECTED", Colors.BOLD_RED),
        "",
        "Manual override initiated.",
        "Do you wish to sever the neural link?",
        "",
        ("EXIT TO DESKTOP?", Colors.BOLD_MAGENTA),
    ]
    box = MessageBox(
        msg, title="INTERRUPT", choices=["RESUME", "EXIT"], border_color=Colors.BOLD_RED
    )
    choice = box.display(stdscr)
    if choice == 1:
        return True  # Should quit
    clear_terminal(stdscr)
    return False  # Should resume


def getch_with_pause(stdscr, game_state, audio, current_slot, current_scene_id):
    """
    Wrapper for stdscr.getch() that intercepts ESC to show the pause menu.
    """
    from engine.pause_menu import show_pause_menu

    while True:
        ch = stdscr.getch()
        if ch == 27:  # ESC key
            stdscr.nodelay(False)
            result = show_pause_menu(
                stdscr, game_state, audio, current_slot, current_scene_id
            )
            stdscr.nodelay(True)
            if result == -999:
                return -999  # Signal to quit to menu
            # If resumed, loop back to wait for a valid game key
            continue
        return ch


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

    # TEST Bypass
    if config.TEST:
        # TEST mode doesn't use player name anymore
        pass

        if config.TEST == "system_reboot":
            from scenes.intro_sequence import system_reboot

            msg = [
                "",
                ("TEST MODE STORY BYPASS", Colors.BOLD_RED),
                "",
                ("Continuing from:", Colors.BOLD_WHITE),
                (f"[{config.TEST}]", Colors.BOLD_WHITE),
            ]
            MessageBox(
                msg, title="ADMIN OVERRIDE", border_color=Colors.BOLD_MAGENTA
            ).display(stdscr, duration=1.0)
            time.sleep(0.5)
            system_reboot(stdscr, game_state)
            return

        try:
            scene = get_scene(str(config.TEST))
            msg = [
                "",
                ("TEST MODE STORY BYPASS", Colors.BOLD_RED),
                "",
                ("Continuing from:", Colors.BOLD_WHITE),
                (f"[{config.TEST}]", Colors.BOLD_WHITE),
            ]
            MessageBox(
                msg, title="ADMIN OVERRIDE", border_color=Colors.BOLD_MAGENTA
            ).display(stdscr, duration=1.0)
            audio.stop_music()
            time.sleep(1)

            current_scene_id = str(config.TEST)
            current_slot = 1
            while current_scene_id:
                scene = get_scene(current_scene_id)

                def getch_wrapper():
                    return getch_with_pause(
                        stdscr, game_state, audio, current_slot, current_scene_id
                    )

                next_scene_id = scene.run(stdscr, game_state, getch_func=getch_wrapper)
                if next_scene_id == -999:
                    break
                current_scene_id = next_scene_id
            return

        except ValueError:
            print_colored(
                f"\n[DEBUG ERROR] Scene '{config.TEST}' not found in registry or intro_sequence.py!",
                Colors.BOLD_RED,
                stdscr=stdscr,
            )
            time.sleep(2)

    current_scene_id = None
    game_state = None
    current_slot = 1

    while True:
        try:
            # load title
            title = load_ascii_art("title.txt")
            audio.play_music("theme.mp3", loop=True, volume=0.5)
            time.sleep(0.5)

            if title:
                menu = GrubMenu(
                    ["Continue", "New Game", "Settings"],
                    title=title,
                    title_menu_spacing=5,
                    vertical_offset=2,
                    glitchify=True,
                )
                choice_index = menu.display(stdscr)
            else:
                print_typing(
                    "FRAGMENTS OF THE LATTICE", 0.03, Colors.GREEN, stdscr=stdscr
                )
                menu = GrubMenu(["Continue", "New Game", "Settings"], title=None)
                choice_index = menu.display(stdscr)

            clear_terminal(stdscr)

            if choice_index == 0:  # Continue
                from scenes.intro_sequence import loading_bar
                from scenes.registry import get_scene_name

                saves = SaveManager.get_all_saves(6)
                choices = []
                has_saves = False
                for i, save in enumerate(saves, 1):
                    if save:
                        has_saves = True
                        state = save["state"]
                        scene_name = get_scene_name(save["scene_id"])
                        choices.append(
                            f"Slot {i}: {len(state.get('identity_fragments', []))} fragments [{scene_name}]"
                        )
                    else:
                        choices.append(f"Slot {i}: [ EMPTY ]")
                choices.append("Cancel")

                if not has_saves:
                    error_msg = [
                        ("NO SAVA DATA FOUND", Colors.BOLD_RED),
                        "",
                        "No encrypted save data detected.",
                        "The save file is empty.",
                        "",
                        ("Returning to main menu...", Colors.BOLD_WHITE),
                    ]
                    error_box = MessageBox(
                        error_msg, title="NO SAVES FOUND", border_color=Colors.BOLD_RED
                    )
                    error_box.display(stdscr, duration=2)
                    clear_terminal(stdscr)
                    continue

                title_lines = [
                    "    SELECT SAVE TO LOAD    ",
                    "===========================",
                ]
                slot_menu = GrubMenu(
                    choices,
                    title=title_lines,
                    title_menu_spacing=3,
                    vertical_offset=2,
                    glitchify=True,
                )
                slot_idx = slot_menu.display(stdscr)
                if slot_idx == 6:  # Cancel
                    clear_terminal(stdscr)
                    continue

                save_data = saves[slot_idx]
                if not save_data:
                    error_msg = [
                        ("ERROR: SLOT EMPTY", Colors.BOLD_RED),
                        "No data in selected slot.",
                    ]
                    MessageBox(
                        error_msg, title="NODE FAILURE", border_color=Colors.BOLD_RED
                    ).display(stdscr, duration=1.5)
                    clear_terminal(stdscr)
                    continue

                current_slot = slot_idx + 1

                audio.stop_music(fadeout_ms=1000)

                # Loading cinematic
                clear_terminal(stdscr)
                loading_bar(
                    stdscr,
                    duration=1,
                    length=40,
                    color=Colors.BOLD_CYAN,
                    title="LOADING SAVE",
                )
                clear_terminal(stdscr)

                game_state = GameState.from_snapshot(save_data["state"])
                current_scene_id = save_data["scene_id"]
                scene_name = get_scene_name(current_scene_id)
                break  # Start scene loop

            elif choice_index == 1:  # New Game
                from scenes.intro_sequence import loading_bar

                saves = SaveManager.get_all_saves(6)
                choices = []
                for i, save in enumerate(saves, 1):
                    if save:
                        state = save["state"]
                        choices.append(
                            f"Slot {i}: {len(state.get('identity_fragments', []))} fragments [IN USE]"
                        )
                    else:
                        choices.append(f"Slot {i}: [ EMPTY ]")
                choices.append("Cancel")
                title_lines = [
                    "    SELECT NEW MEMORY SLOT    ",
                    "==============================",
                ]
                slot_menu = GrubMenu(
                    choices,
                    title=title_lines,
                    title_menu_spacing=3,
                    vertical_offset=2,
                    glitchify=True,
                )
                slot_idx = slot_menu.display(stdscr)
                if slot_idx == 6:  # Cancel
                    clear_terminal(stdscr)
                    continue

                current_slot = slot_idx + 1

                if saves[slot_idx]:
                    confirm_msg = [
                        ("WARNING: PREVIOUS SAVE WILL BE ERASED", Colors.BOLD_RED),
                        "",
                        f"Initiating a new save on Slot {current_slot}",
                        "will irreversibly erase the previous save.",
                        "",
                        ("PROCEED WITH OVERWRITE?", Colors.BOLD_MAGENTA),
                    ]
                    confirm_box = MessageBox(
                        confirm_msg,
                        title="SAVE OVERWRITE",
                        choices=["GO BACK", "PROCEED"],
                        border_color=Colors.BOLD_MAGENTA,
                    )
                    confirm_choice = confirm_box.display(stdscr)
                    if confirm_choice == 0:  # GO BACK
                        clear_terminal(stdscr)
                        continue
                    SaveManager.delete_save(slot=current_slot)  # Clear old data

                game_state = GameState()  # Reset local state
                audio.stop_music(fadeout_ms=1000)
                clear_terminal(stdscr)
                loading_bar(
                    stdscr,
                    duration=1.5,
                    length=40,
                    color=Colors.BOLD_MAGENTA,
                    title="NEW GAME",
                )
                clear_terminal(stdscr)

                # Full onboarding for New Game
                time.sleep(1)

                # Global pause-aware getch for the intro sequence
                def intro_getch():
                    return getch_with_pause(
                        stdscr, game_state, audio, current_slot, "intro"
                    )

                onboarding(stdscr, getch_func=intro_getch)
                time.sleep(1)
                initiating_sequence(stdscr, getch_func=intro_getch)
                clear_terminal(stdscr)
                display_success_message(stdscr, getch_func=intro_getch)
                memory_load_prompt(stdscr, getch_func=intro_getch)

                corrupt_ascii = []
                for i in range(1, 4):
                    corrupt_ascii.append(load_ascii_art(f"intro_glitch_{i}.txt"))
                corruption_flash(stdscr, corrupt_ascii)
                
                # Add loading screen after corruption flash
                from scenes.intro_sequence import loading_screen
                loading_screen(stdscr, duration=2.5)

                time.sleep(2)
                if config.TEST and config.TEST != "system_reboot":
                    # TEST mode doesn't use player name anymore
                    pass
                else:
                    # system_reboot doesn't return a name anymore, just use default
                    pass

                current_scene_id = "scene1_identity_sequence"
                break  # Start scene loop

            elif choice_index == 2:  # Settings
                while True:
                    music_text = "ON" if config.ENABLE_MUSIC else "OFF"
                    sound_text = "ON" if config.ENABLE_SOUNDS else "OFF"
                    anim_text = "OFF" if config.SKIP_ANIMATIONS else "ON"

                    choices = [
                        f"Music: {music_text}",
                        f"Sound FX: {sound_text}",
                        f"Animations: {anim_text}",
                        "Back",
                    ]

                    title_lines = [" SYSTEM SETTINGS ", "================="]
                    settings_menu = GrubMenu(
                        choices,
                        title=title_lines,
                        title_menu_spacing=3,
                        vertical_offset=2,
                        glitchify=False,
                    )
                    sel = settings_menu.display(stdscr)

                    if sel == 0:
                        config.ENABLE_MUSIC = not config.ENABLE_MUSIC
                        if not config.ENABLE_MUSIC:
                            audio.stop_music()
                        else:
                            audio.play_music("theme.mp3", loop=True, volume=0.5)
                    elif sel == 1:
                        config.ENABLE_SOUNDS = not config.ENABLE_SOUNDS
                        if config.ENABLE_SOUNDS:
                            audio.play_sound("beep.mp3")
                    elif sel == 2:
                        config.SKIP_ANIMATIONS = not config.SKIP_ANIMATIONS
                    elif sel == 3:
                        break

                clear_terminal(stdscr)
                continue
        except KeyboardInterrupt:
            if handle_interrupt(stdscr):
                return

    # --- Scene Progression Loop ---
    while current_scene_id:
        try:
            scene = get_scene(current_scene_id)

            # Create a localized wrapper that has access to all required state
            # This allows scenes/elements to trigger the pause menu without knowing about SaveManager or GameState
            def getch_wrapper():
                return getch_with_pause(
                    stdscr, game_state, audio, current_slot, current_scene_id
                )

            # Execute the scene and get the ID of the next one
            next_scene_id = scene.run(stdscr, game_state, getch_func=getch_wrapper)

            if next_scene_id == -999:
                # Quit to main menu
                current_scene_id = None
                clear_terminal(stdscr)
                continue  # Back to title loop

            # Update current scene ID for next iteration
            current_scene_id = next_scene_id

            # Auto-save progress if we are transitioning to a new scene
            if current_scene_id:
                SaveManager.save_game(game_state, current_scene_id, slot=current_slot)

        except KeyboardInterrupt:
            if handle_interrupt(stdscr):
                return
        except Exception as e:
            from engine.core.logger import game_logger

            game_logger.error(f"Failed to execute scene {current_scene_id}: {e}")
            break

    # --- Game Summary / End Phase ---
    clear_terminal(stdscr)
    from engine.ui.end_screen import EndScreen

    summary = EndScreen(game_state)
    summary.display(stdscr)

    print_centered("[ TO BE CONTINUED... ]", Colors.BOLD_MAGENTA, stdscr=stdscr)
    time.sleep(3)


def main_curses(stdscr):
    from engine.core.audio import AudioManager
    from engine.core.logger import game_logger
    from engine.ui.ui_utils import ensure_min_terminal
    from scenes.intro_sequence import logo_animation, startup_screen

    # IMPROVE ESC KEY RESPONSIVENESS ON WINDOWS
    try:
        curses.set_escdelay(25)
    except:
        pass

    time.sleep(1)

    try:
        # Start atmospheric static immediately
        audio = AudioManager()
        audio.play_music("vhs_static.mp3", loop=True, volume=0.8)

        # 0. Show company logo animation
        if not config.SKIP_STARTUP:
            logo_animation(stdscr)

        # 1. Calibrate terminal
        ensure_min_terminal(stdscr)
        time.sleep(1)

        # 1.5. Disclaimer
        if not config.SKIP_STARTUP:
            from scenes.intro_sequence import glitch_ascii_animation

            disclaimer_ascii = load_ascii_art("disclaimer.txt")
            disclaimer_text = (
                "\n\n\n\nSome individuals may experience seizures or loss of consciousness\n"
                "when exposed to certain light patterns or flashing lights.\n"
                "This game contains bright visuals, rapidly flashing colors, and\n"
                "glitch effects that may trigger such reactions.\n\n"
                "If you have a history of epilepsy, photosensitivity, or seizures,\n"
                "consult a medical professional before playing and stop immediately\n"
                "if you feel dizzy, disoriented, or unwell.\n\n"
                "Player discretion is strongly advised."
            )

            prompt_text = "\n\n\nPRESS [ENTER] TO CONTINUE"

            # Pass as a list of (text, color, delay) blocks
            glitch_blocks = [
                (disclaimer_ascii, Colors.BOLD_RED, 0),
                (disclaimer_text, Colors.WHITE, 0),
                (prompt_text, Colors.BOLD_MAGENTA, 2.0),  # Reveal 4 seconds later
            ]
            glitch_ascii_animation(
                stdscr, glitch_blocks, wait_for_key=True, justify_center=True
            )
            audio.stop_music(fadeout_ms=500)
            time.sleep(1)

        # 2. Show startup screen inside curses
        if not config.SKIP_STARTUP:
            startup_screen(stdscr, 15)
            time.sleep(2)

        # 3. Run the game
        run_game(stdscr)
    except KeyboardInterrupt:
        game_logger.info("User interrupted")
    except Exception as e:
        game_logger.exception("Fatal error")
        try:
            os.system("reset")
        except:
            pass
        print(f"Lattice crashed. Check logs/fotd.log\nError: {e}")


if __name__ == "__main__":
    from engine.core.logger import setup_logging

    setup_logging()

    # Start the game
    curses.wrapper(main_curses)
