import curses
import time


def show_pause_menu(stdscr, game_state, audio, current_slot, current_scene_id):
    from engine.core.save_manager import SaveManager
    from engine.ui.console_effects import CursesColors

    h, w = stdscr.getmaxyx()
    audio.pause_all()

    win = curses.newwin(h, w, 0, 0)
    win.keypad(True)
    win.nodelay(False)
    curses.curs_set(0)

    curses_colors = CursesColors()
    COLOR_ACCENT = getattr(curses_colors, "ansi_1m36", curses.A_BOLD)
    COLOR_DIM    = getattr(curses_colors, "ansi_0m37", curses.A_NORMAL)
    COLOR_SELECT = curses.A_REVERSE | curses.A_BOLD

    box_h = 14
    box_w = 42
    start_y = (h - box_h) // 2
    start_x = (w - box_w) // 2

    options = ["Resume", "Save & Continue", "Quit to Menu"]
    selected = 0
    status_msg = ""
    confirm_quit = False

    def draw():
        win.erase()

        # Border
        win.attron(COLOR_ACCENT)
        win.addstr(start_y, start_x, "╔" + "═" * (box_w - 2) + "╗")
        for i in range(1, box_h - 1):
            win.addstr(start_y + i, start_x, "║")
            win.addstr(start_y + i, start_x + box_w - 1, "║")
        win.addstr(start_y + box_h - 1, start_x, "╚" + "═" * (box_w - 2) + "╝")
        win.attroff(COLOR_ACCENT)

        # Title
        title = "[ PAUSE MENU ]"
        win.attron(COLOR_ACCENT)
        win.addstr(start_y, start_x + (box_w - len(title)) // 2, title)
        win.attroff(COLOR_ACCENT)

        # Separator under title
        win.attron(COLOR_DIM | curses.A_DIM)
        win.addstr(start_y + 2, start_x + 1, "─" * (box_w - 2))
        win.attroff(COLOR_DIM | curses.A_DIM)

        # Options
        for i, option in enumerate(options):
            y = start_y + 4 + i * 2
            x = start_x + (box_w - len(option)) // 2
            if i == selected:
                win.attron(COLOR_ACCENT)
                win.addstr(y, x - 2, ">")
                win.attroff(COLOR_ACCENT)
                win.attron(COLOR_SELECT)
                win.addstr(y, x, option)
                win.attroff(COLOR_SELECT)
            else:
                win.attron(COLOR_DIM)
                win.addstr(y, x, option)
                win.attroff(COLOR_DIM)

        # Separator above footer
        win.attron(COLOR_DIM | curses.A_DIM)
        win.addstr(start_y + box_h - 3, start_x + 1, "─" * (box_w - 2))
        win.attroff(COLOR_DIM | curses.A_DIM)

        # Footer
        if status_msg:
            win.attron(COLOR_ACCENT)
            win.addstr(start_y + box_h - 2, start_x + (box_w - len(status_msg)) // 2, status_msg)
            win.attroff(COLOR_ACCENT)
        else:
            hint = "↑↓ Navigate   Enter Select"
            win.attron(COLOR_DIM | curses.A_DIM)
            win.addstr(start_y + box_h - 2, start_x + (box_w - len(hint)) // 2, hint)
            win.attroff(COLOR_DIM | curses.A_DIM)

        win.refresh()

    while True:
        draw()
        key = win.getch()

        if key == 27:  # ESC — always resume
            confirm_quit = False
            status_msg = ""
            break

        elif key in [curses.KEY_UP, curses.KEY_DOWN]:
            selected = (selected + (-1 if key == curses.KEY_UP else 1)) % len(options)
            status_msg = ""
            confirm_quit = False

        elif key in [10, 13]:  # Enter
            if confirm_quit:
                audio.resume_all()
                del win
                return -999

            elif selected == 0:  # Resume
                break

            elif selected == 1:  # Save & Continue
                if game_state and current_scene_id:
                    SaveManager.save_game(game_state, current_scene_id, slot=current_slot)
                    status_msg = "✓  PROGRESS SAVED"
                    draw()
                    time.sleep(0.8)
                    break
                else:
                    status_msg = "✗  NO ACTIVE GAME"

            elif selected == 2:  # Quit to Menu
                confirm_quit = True
                status_msg = "PRESS ENTER AGAIN TO CONFIRM"

    audio.resume_all()
    del win
    stdscr.touchwin()
    stdscr.refresh()
    return 0