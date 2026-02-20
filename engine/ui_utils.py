import curses
import sys
import os
from engine.console_effects import Colors, clear_terminal
from engine.audio import AudioManager

audio = AudioManager()

class ScreenBuffer:
    """Saves and restores the terminal screen state."""
    def __init__(self, stdscr):
        self.stdscr = stdscr
        h, w = stdscr.getmaxyx()
        self.saved_window = curses.newwin(h, w, 0, 0)

    def save(self):
        self.saved_window.overwrite(self.stdscr)

    def restore(self):
        self.stdscr.clear()
        self.saved_window.overwrite(self.stdscr)
        self.stdscr.refresh()

def show_pause_menu(stdscr):
    """Displays the pause menu and handles screen persistence."""
    from engine.elements import MessageBox
    
    # Save current screen
    buffer = ScreenBuffer(stdscr)
    buffer.save()
    
    # Clear for menu
    stdscr.clear()
    stdscr.refresh()

    msg = [
        ("SYSTEM SUSPENDED", Colors.BOLD_YELLOW),
        "",
        "Identity synchronization paused.",
        "Neural link held in stasis.",
        "",
        ("RESUME      - Return to Lattice", Colors.BOLD_WHITE),
        ("TERMINATE   - Force Disconnect", Colors.BOLD_RED)
    ]
    
    menu = MessageBox(
        msg, 
        title="PAUSE", 
        choices=["RESUME", "TERMINATE"], 
        border_color=Colors.BOLD_YELLOW
    )
    
    choice = menu.display(stdscr)

    if choice == 0: # Resume
        buffer.restore()
        return True
    elif choice == 1: # Terminate
        if confirm_quit_menu(stdscr):
            sys.exit(0)
        else:
            buffer.restore()
            return True
    
    # Fallback
    buffer.restore()
    return True

def confirm_quit_menu(stdscr):
    """Displays a quit confirmation box."""
    from engine.elements import MessageBox
    
    msg = [
        ("TERMINATE CONNECTION?", Colors.BOLD_RED),
        "",
        "Unsaved fragments will be lost.",
        "Neural feedback may occur.",
        "",
        "Awaiting confirmation..."
    ]
    
    menu = MessageBox(
        msg, 
        title="DISCONNECT", 
        choices=["CANCEL", "CONFIRM"], 
        border_color=Colors.RED
    )
    
    choice = menu.display(stdscr)
    return choice == 1
