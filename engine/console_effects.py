import os
import shutil
import time
import random
import curses
import sys
from typing import List, Union
from engine.audio import AudioManager

audio = AudioManager()

class Colors:
    RESET = "RESET"
    BLACK = "0;30"
    RED = "0;31"
    GREEN = "0;32"
    YELLOW = "0;33"
    BLUE = "0;34"
    MAGENTA = "0;35"
    CYAN = "1;36"
    WHITE = "0;37"
    BOLD_BLACK = "1;30"
    BOLD_RED = "1;31"
    BOLD_GREEN = "1;32"
    BOLD_YELLOW = "1;33"
    BOLD_BLUE = "1;34"
    BOLD_MAGENTA = "1;35"
    BOLD_CYAN = "1;36"
    BOLD_WHITE = "1;37"

class ANSIColors:
    RESET = "\033[0m"
    BOLD_GREEN = "\033[1;32m"
    CYAN = "\033[1;36m"

class CursesColors:
    def __init__(self):
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()

            self.color_map = {
                "0;30": curses.COLOR_BLACK,
                "0;31": curses.COLOR_RED,
                "0;32": curses.COLOR_GREEN,
                "0;33": curses.COLOR_YELLOW,
                "0;34": curses.COLOR_BLUE,
                "0;35": curses.COLOR_MAGENTA,
                "0;36": curses.COLOR_CYAN,
                "0;37": curses.COLOR_WHITE,
                "1;30": curses.COLOR_BLACK,
                "1;31": curses.COLOR_RED,
                "1;32": curses.COLOR_GREEN,
                "1;33": curses.COLOR_YELLOW,
                "1;34": curses.COLOR_BLUE,
                "1;35": curses.COLOR_MAGENTA,
                "1;36": curses.COLOR_CYAN,
                "1;37": curses.COLOR_WHITE,
            }

            self.attribute_map = {"1": curses.A_BOLD}

            for i, (ansi_code, curses_color) in enumerate(self.color_map.items()):
                if i + 1 < curses.COLOR_PAIRS:
                    curses.init_pair(i + 1, curses_color, -1)
                    attr = self.attribute_map.get(ansi_code.split(";")[0], 0)
                    setattr(self, f"ansi_{ansi_code.replace(';', 'm')}", curses.color_pair(i + 1) | attr)

# Corruption mapping
CORRUPTION_MAP = {
    "a": "@","b": "8","c": "(","d": "Ð","e": "3","f": "ƒ","g": "9","h": "#",
    "i": "1","j": "]","k": "X","l": "1","m": "^^","n": "Ñ","o": "0","p": "¶",
    "q": "9","r": "®","s": "$","t": "+","u": "µ","v": "√","w": "ω","x": "×",
    "y": "¥","z": "2"
}

colors = [
    Colors.RESET, Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.MAGENTA,
    Colors.CYAN, Colors.WHITE, Colors.BOLD_RED, Colors.BOLD_GREEN, Colors.BOLD_YELLOW,
    Colors.BOLD_BLUE, Colors.BOLD_MAGENTA, Colors.BOLD_CYAN, Colors.BOLD_WHITE, Colors.BOLD_BLACK
]

def get_colors():
    return colors

_curses_colors_instance = None

def get_curses_color(ansi_color: str):
    """Convert ANSI string to curses attribute."""
    global _curses_colors_instance
    if _curses_colors_instance is None:
        _curses_colors_instance = CursesColors()
    return map_ansi_to_curses(ansi_color, _curses_colors_instance)

def map_ansi_to_curses(ansi_color: str, curses_colors: CursesColors):
    if ansi_color is None or ansi_color == Colors.RESET:
        return curses.A_NORMAL
    code = ansi_color.replace(";", "m")
    attr_name = f"ansi_{code}"
    return getattr(curses_colors, attr_name, curses.A_NORMAL)

def _glitchify(text: str, intensity: float = 0.1) -> str:
    chars = list(text)
    glitch_chars = ["#", "@", "%", "&", "$", "*", "+", "?", "▒", "░", "▓", "!", "/", "|"]
    for i, ch in enumerate(chars):
        if not ch.isspace() and random.random() < intensity:
            chars[i] = random.choice(glitch_chars)
    return "".join(chars)

# ---------- Printing Functions ---------- #

def normal_print_colored(
    text: str,
    color: str = ANSIColors.RESET,
    end: str = "\n",
    center: bool = False,
    width: int = None
):
    if width is None:
        width, _ = shutil.get_terminal_size((80, 24))

    if center:
        text = text.center(width)

    sys.stdout.write(f"{color}{text}{ANSIColors.RESET}{end}")
    sys.stdout.flush()

def print_colored(
    text: str,
    color: str = Colors.RESET,
    end: str = "\n",
    stdscr=None,
    y: int = None,
    x: int = None,
    sound: bool = False
):
    if stdscr is None:
        raise ValueError("Curses stdscr must be passed for printing.")

    curses_colors = CursesColors()
    attr = map_ansi_to_curses(color, curses_colors)

    try:
        if y is not None and x is not None:
            stdscr.addstr(y, x, text, attr)
            if end:
                stdscr.addstr(end, attr)
        else:
            stdscr.addstr(text, attr)
            if end:
                stdscr.addstr(end, attr)

        if sound:
            audio.play_sound("beep.mp3", loop=False, volume=1)

    except curses.error:
        pass

    stdscr.refresh()


def print_typing(
    text: str,
    seconds_per_char: float = 0.03,
    color: str = Colors.RESET,
    stdscr=None,
    y: int = None,
    x: int = None,
    end: str = "\n",
    sound: bool = True
):
    if stdscr is None:
        raise ValueError("Curses stdscr must be passed for printing.")

    curses_colors = CursesColors()
    attr = map_ansi_to_curses(color, curses_colors)

    if sound:
        audio.play_sound("typing.mp3", loop=True, volume=1)

    # Enable non-blocking input for skip detection
    stdscr.nodelay(True)
    skip = False

    for idx, ch in enumerate(text):
        if not skip:
            # Skip detection: Enter (10, 13), Space (32), 's' keyboard key
            try:
                key = stdscr.getch()
                if key in [10, 13, 32, ord('s')]:
                    skip = True
                    if sound:
                        audio.stop_sound("typing.mp3")
            except:
                pass

        try:
            if y is not None and x is not None:
                stdscr.addch(y, x + idx, ch, attr)
            else:
                stdscr.addch(ch, attr)
        except curses.error:
            pass
        
        stdscr.refresh()
        if not skip:
            time.sleep(max(0.0, seconds_per_char))


    # Reset nodelay, stop sound, and flush input buffer
    stdscr.nodelay(False)
    if not skip and sound:
        audio.stop_sound("typing.mp3")
    
    # NEW: Wipe the input buffer so spamming 'Enter' doesn't skip the next menu
    curses.flushinp()

    # Add the "end" string
    if end:
        try:
            stdscr.addstr(end, attr)
        except curses.error:
            pass
        stdscr.refresh()


def print_glitch(
    text: str,
    base_color: str = Colors.MAGENTA,
    intensity: float = 0.15,
    typing: bool = False,
    stdscr=None,
    y: int = None,
    x: int = None,
    end: str = "\n"
):
    if stdscr is None:
        raise ValueError("Curses stdscr must be passed for printing.")

    curses_colors = CursesColors()
    attr = map_ansi_to_curses(base_color, curses_colors)

    scrambled = _glitchify(text, intensity=intensity)

    if typing:
        print_typing(scrambled, 0.03, base_color, stdscr=stdscr, y=y, x=x, end=end)
    else:
        for idx, ch in enumerate(scrambled):
            try:
                if y is not None and x is not None:
                    stdscr.addch(y, x + idx, ch, attr)
                else:
                    stdscr.addch(ch, attr)
            except curses.error:
                pass

        # Add `end` (newline or nothing) after glitch text
        if end:
            try:
                stdscr.addstr(end)
            except curses.error:
                pass

        stdscr.refresh()



def echo_line(text: str, seconds_per_char: float = 0.03, color: str = Colors.BOLD_MAGENTA, intensity: float = 0.15, stdscr=None, y: int = None, x: int = None, end: str = ""):
    if stdscr is None:
        raise ValueError("Curses stdscr must be passed for printing.")

    curses_colors = CursesColors()
    attr = map_ansi_to_curses(color, curses_colors)

    # Track current x position if coordinates given, else None
    current_x = x if x is not None else None

    # Enable non-blocking input for pause detection
    stdscr.nodelay(True)

    for ch in text:
        try:
            key = stdscr.getch()
        except:
            pass

        lower = ch.lower()
        # Get replacement char from corruption map or original char
        char = CORRUPTION_MAP.get(lower, ch) if random.random() < intensity else ch

        # Ensure char is exactly one character
        if len(char) != 1:
            # if corruption map returns multi-char string, fallback to original char
            char = ch

        try:
            if y is not None and current_x is not None:
                stdscr.addch(y, current_x, char, attr)
                current_x += 1
            else:
                stdscr.addch(char, attr)
        except curses.error:
            pass

        stdscr.refresh()
        audio.play_sound("beep.mp3", volume=1)
        time.sleep(max(0.0, random.uniform(0.01, seconds_per_char + 0.05)))

    # Reset nodelay
    stdscr.nodelay(False)

    # Handle end string by printing it normally if given
    if end:
        stdscr.addstr(end)
        stdscr.refresh()


def print_centered(content: Union[str, List[str]], color: str = Colors.RESET, stdscr=None, offset: int = 0):
    if stdscr is None:
        raise ValueError("Curses stdscr must be passed for printing.")

    if isinstance(content, str):
        lines = content.splitlines()
    else:
        lines = content

    h, w = stdscr.getmaxyx()
    start_y = max((h - len(lines)) // 2 - offset, 0)
    for i, line in enumerate(lines):
        x = max((w - len(line)) // 2, 0)
        print_colored(line, color, stdscr=stdscr, y=start_y + i, x=x)

def clear_terminal(stdscr=None):
    if stdscr is None:
        raise ValueError("Curses stdscr must be passed for clearing.")
    stdscr.clear()
    stdscr.refresh()

def clear_main_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def full_screen_glitch(stdscr, ascii_art_blocks: list[str] | None = None, frames: int = 180, frame_delay: float = 0.03) -> None:
    from engine.console_effects import Colors, CursesColors, clear_terminal
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:',.<>/?\\|█▓▒░"

    ascii_index = 0
    ascii_frame_counter = 0
    current_art_lines: list[str] | None = None

    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    curses_colors = CursesColors()

    color_attrs = [
        curses_colors.ansi_0m31, curses_colors.ansi_0m32, curses_colors.ansi_0m33,
        curses_colors.ansi_0m34, curses_colors.ansi_0m35, curses_colors.ansi_0m36,
        curses_colors.ansi_0m37, curses_colors.ansi_1m31, curses_colors.ansi_1m32,
        curses_colors.ansi_1m33, curses_colors.ansi_1m34, curses_colors.ansi_1m35,
        curses_colors.ansi_1m36, curses_colors.ansi_1m37
    ]

    audio.play_music("glitch.mp3")
    for frame in range(frames):
        stdscr.erase()

        # pick a random color attribute
        color_attr = random.choice(color_attrs)

        # load ASCII art if it's time
        if ascii_art_blocks:
            if current_art_lines is None and ascii_index < len(ascii_art_blocks):
                current_art_lines = ascii_art_blocks[ascii_index].splitlines()
                ascii_frame_counter = frames // 3

        # generate glitch screen
        glitch_screen = [
            "".join(random.choice(charset) for _ in range(w))
            for _ in range(h)
        ]

        # overlay ASCII art if active
        if current_art_lines and ascii_frame_counter > 0:
            art_h = len(current_art_lines)
            art_w = max(len(line) for line in current_art_lines)

            start_row = max((h - art_h) // 2, 0)
            start_col = max((w - art_w) // 2, 0)

            for i, art_line in enumerate(current_art_lines):
                if 0 <= start_row + i < h:
                    line_as_list = list(glitch_screen[start_row + i])
                    for j, ch in enumerate(art_line):
                        if 0 <= start_col + j < w:
                            line_as_list[start_col + j] = ch
                    glitch_screen[start_row + i] = "".join(line_as_list)

            ascii_frame_counter -= 1
            if ascii_frame_counter == 0:
                ascii_index += 1
                current_art_lines = None

        # draw frame using curses colors
        for y, line in enumerate(glitch_screen):
            if y < h:
                try:
                    stdscr.addstr(y, 0, line[:w], color_attr)
                except curses.error:
                    pass

        stdscr.refresh()
        time.sleep(frame_delay)
    audio.stop_music()
    clear_terminal(stdscr)