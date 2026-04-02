import curses
import sys
import time
import os
from typing import Tuple

from engine.ui.console_effects import Colors, clear_terminal
from engine.ui.elements import MessageBox
from engine.core.audio import AudioManager

def flush_input_buffer(stdscr):
    """Flush all pending input from the buffer."""
    stdscr.nodelay(True)
    try:
        while stdscr.getch() != -1:
            pass
    finally:
        stdscr.nodelay(False)
        curses.flushinp()

def _is_true_fullscreen_f11() -> bool:
    """
    STRICT F11 FULLSCREEN ONLY (no maximized windows).
    """
    if os.name != 'nt':
        return True  # Non-Windows always passes
    
    try:
        import ctypes
        from ctypes import wintypes
        
        user32 = ctypes.windll.user32
        
        hwnd = user32.GetForegroundWindow()
        if not hwnd:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        
        if hwnd:
            # Check 1: NO window decorations (true fullscreen hallmark)
            style = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
            
            # Must be popup-style (no caption, borders)
            is_popup_style = (
                (style & 0x80000000) and  # WS_POPUP
                not (style & 0x00C00000)  # No WS_CAPTION
            )
            
            if is_popup_style:
                return True
            
            # Check 2: PERFECT fullscreen coverage (0px tolerance)
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            
            monitor = user32.MonitorFromWindow(hwnd, 2)
            if monitor:
                class MONITORINFO(ctypes.Structure):
                    _fields_ = [
                        ("cbSize", wintypes.DWORD),
                        ("rcMonitor", wintypes.RECT),
                        ("rcWork", wintypes.RECT),
                        ("dwFlags", wintypes.DWORD)
                    ]
                
                mi = MONITORINFO()
                mi.cbSize = ctypes.sizeof(MONITORINFO)
                
                if user32.GetMonitorInfoW(monitor, ctypes.byref(mi)):
                    monitor_rect = mi.rcMonitor  # Full monitor rect
                    
                    # PERFECT fullscreen match
                    fullscreen = (
                        rect.left == monitor_rect.left and
                        rect.top == monitor_rect.top and
                        rect.right == monitor_rect.right and
                        rect.bottom == monitor_rect.bottom
                    )
                    
                    return fullscreen
        
        return False
        
    except Exception:
        return False

def ensure_min_terminal(stdscr, min_height=40, min_width=120, getch_func=None):
    """
    F11 FULLSCREEN ONLY + minimum size.
    """
    audio = AudioManager()
    # Only start if not already playing from the logo phase
    if not (audio.current_track and audio.current_track.endswith("vhs_static.mp3")):
        audio.play_music("vhs_static.mp3", loop=True, volume=0.8)

    while True:
        curses.update_lines_cols()
        h, w = stdscr.getmaxyx()
        is_f11_fullscreen = _is_true_fullscreen_f11()

        # ALL requirements: size + TRUE F11 fullscreen
        if h >= min_height and w >= min_width and is_f11_fullscreen:
            break

        stdscr.clear()

        # Error indicators
        size_fail = h < min_height or w < min_width
        fullscreen_fail = not is_f11_fullscreen

        lines = [
            " TERMINAL CALIBRATION REQUIRED ",
            "================================",
            "",
            f" [Current Resolution: {w}x{h}] " + (f"(Required: {min_width}x{min_height})" if size_fail else "[OK]"),
            f" [Fullscreen Mode: {'ENABLED' if is_f11_fullscreen else 'DISABLED'}] " + ( "(Press F11 for Fullscreen)" if fullscreen_fail else "[OK]"),
            "",
            " This game requires a large, full-screen terminal to display properly. ",
            " Please press [F11] to enter True Fullscreen mode (not maximized). ",
            "",
            " [R] - RE-SCAN",
            " [Q] - QUIT",
            "",
        ]

        start_y = max((h - len(lines)) // 2, 0)
        for i, line in enumerate(lines):
            try:
                attr = curses.A_BOLD
                if "SIZE" in line and size_fail:
                    attr |= curses.A_REVERSE
                if "MODE" in line and fullscreen_fail:
                    attr |= curses.A_REVERSE
                stdscr.addstr(start_y + i, max((w - len(line)) // 2, 0), line, attr)
            except:
                pass

        stdscr.refresh()
        stdscr.nodelay(False)
        getch = getch_func or stdscr.getch
        ch = getch()
        
        if ch == -999: return  # Quit signal
        if ch in [ord('q'), ord('Q')]:
            sys.exit(0) 
        elif ch in [ord('r'), ord('R')]:
            continue

        time.sleep(0.1)

    # Calibration Successful Screen - SAFE COLOR VERSION
    stdscr.clear()
    curses.update_lines_cols()
    h, w = stdscr.getmaxyx()
    
    curses.curs_set(0)
    stdscr.nodelay(False)
    
    success_lines = [
        " [ TERMINAL CALIBRATION SUCCESSFUL ] ",
        "=====================================",
        "",
        " Terminal configured successfully. ",
        " Verification complete. Loading game... ",
        ""
    ]
    
    start_y = max((h - len(success_lines)) // 2, 0)
    
    for i, line in enumerate(success_lines):
        try:
            x_pos = max((w - len(line)) // 2, 0)
            
            if "[" in line or "=" in line:
                # Use ANSI-style bold + green (matches your existing Colors system)
                stdscr.addstr(start_y + i, x_pos, line, curses.A_BOLD)
            else:
                stdscr.addstr(start_y + i, x_pos, line, curses.A_NORMAL)
                
        except curses.error:
            stdscr.addstr(start_y + i, x_pos, line)
    
    stdscr.refresh()
    time.sleep(2.0)

    stdscr.clear()
    stdscr.refresh()



