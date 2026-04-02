import curses
import time

def show_pause_menu(stdscr, game_state, audio, current_slot, current_scene_id):
    """
    Displays a floating pause menu centered on a full-screen overlay.
    This wipes the screen (temporarily) to focus entirely on the menu.
    """
    from engine.core.save_manager import SaveManager
    
    h, w = stdscr.getmaxyx()
    
    # 1. Start audio pause
    audio.pause_all()

    # Cover the entire screen
    win = curses.newwin(h, w, 0, 0)
    win.keypad(True)
    win.nodelay(False)
    curses.curs_set(0)

    # Box dimensions (fixed size as requested)
    box_h = 12
    box_w = 40
    start_y = (h - box_h) // 2
    start_x = (w - box_w) // 2

    options = ["Resume", "Save & Continue", "Quit to Menu"]
    selected = 0
    status_msg = ""

    while True:
        win.erase()
        
        # Draw the centered box
        win.attron(curses.A_BOLD)
        
        # Draw borders of the inner box
        # Top
        win.addstr(start_y, start_x, "╔" + "═" * (box_w - 2) + "╗")
        # Sides
        for i in range(1, box_h - 1):
            win.addstr(start_y + i, start_x, "║")
            win.addstr(start_y + i, start_x + box_w - 1, "║")
        # Bottom
        win.addstr(start_y + box_h - 1, start_x, "╚" + "═" * (box_w - 2) + "╝")
        
        # Title inside the box top
        title = " PAUSED "
        win.addstr(start_y, start_x + (box_w - len(title)) // 2, title)
        win.attroff(curses.A_BOLD)

        # Options relative to the box
        for i, option in enumerate(options):
            x = start_x + (box_w - len(option)) // 2
            y = start_y + 4 + i * 2
            if i == selected:
                win.attron(curses.A_REVERSE | curses.A_BOLD)
                win.addstr(y, x, option)
                win.attroff(curses.A_REVERSE | curses.A_BOLD)
            else:
                win.addstr(y, x, option)

        # Status / Feedback line at the bottom of the box
        if status_msg:
            win.addstr(start_y + box_h - 2, start_x + (box_w - len(status_msg)) // 2, status_msg, curses.A_BOLD)
        else:
            hint = "[Enter] Select | [Esc] Resume"
            win.addstr(start_y + box_h - 2, start_x + (box_w - len(hint)) // 2, hint, curses.A_DIM)

        win.refresh()

        key = win.getch()

        if key == 27: # ESC
            break
        elif key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
            status_msg = ""
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
            status_msg = ""
        elif key in [10, 13]: # Enter
            if selected == 0: # Resume
                break
            elif selected == 1: # Save
                if game_state and current_scene_id:
                    SaveManager.save_game(game_state, current_scene_id, slot=current_slot)
                    status_msg = "SUCCESS: GAME SAVED"
                    win.refresh()
                    time.sleep(0.8)
                    break
                else:
                    status_msg = "ERROR: NO GAME ACTIVE"
                    win.refresh()
            elif selected == 2: # Quit
                status_msg = "CONFIRM: PRESS ENTER AGAIN"
                win.refresh()
                confirm = win.getch()
                if confirm in [10, 13]:
                    # 2. Finish by resuming audio
                    audio.resume_all()
                    del win
                    return -999
                else:
                    status_msg = ""

    # Cleanup: the full-screen window is deleted and the standard screen is restored
    # 2. Finish by resuming audio
    audio.resume_all()

    del win
    stdscr.touchwin()
    stdscr.refresh()
    return 0