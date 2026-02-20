import curses
import time
import random

from engine.audio import *
from engine.console_effects import _glitchify, Colors, CursesColors

audio = AudioManager()


class GrubMenu:
    def __init__(
            self,
            options: list[str],
            title: str | None = None,
            glitchify: bool = False,
            glitch_intensity: float = 0.15,
            vertical_offset: int = 0,       # shift entire block up/down
            title_menu_spacing: int = 2     # lines between title and menu
    ):
        self.options = options
        self.selected_index = 0
        self.glitchify = glitchify
        self.glitch_intensity = glitch_intensity
        self.vertical_offset = vertical_offset
        self.title_menu_spacing = title_menu_spacing

        if isinstance(title, str):
            self.title_lines = title.splitlines()
        else:
            self.title_lines = title

    def display(self, stdscr=None) -> int:
        if stdscr is None:
            return curses.wrapper(self._curses_loop)
        else:
            return self._curses_loop(stdscr)

    def _curses_loop(self, stdscr):
        curses.curs_set(0)
        curses_colors = CursesColors()
        stdscr.nodelay(True)
        stdscr.keypad(True)

        h, w = stdscr.getmaxyx()
        title_lines = self.title_lines if self.title_lines else []

        last_flash_time = time.time()
        flash_interval = 4  # idle time between bursts
        flash_duration = 0.01  # duration of each flash
        flash_pause = 0.05
        flashes_per_burst = 2

        while True:
            # Check for input before clearing if we want to avoid flicker
            key = stdscr.getch()
            if key == curses.KEY_UP and self.selected_index > 0:
                self.selected_index -= 1
            elif key == curses.KEY_DOWN and self.selected_index < len(self.options) - 1:
                self.selected_index += 1
            elif key in [10, 13]:  # Enter
                audio.play_sound("beep.mp3")
                return self.selected_index

            stdscr.clear()
            current_time = time.time()

            # Check if we should start a new burst
            if current_time - last_flash_time >= flash_interval:
                # Run two flashes with a pause in between
                for flash_idx in range(flashes_per_burst):
                    # Draw title with glitch
                    start_y = max((h - len(title_lines) - len(
                        self.options) - self.title_menu_spacing) // 2 - self.vertical_offset, 0)
                    for i, line in enumerate(title_lines):
                        x_start = max((w - len(line)) // 2, 0)
                        for idx, ch in enumerate(line):
                            r = random.random()
                            if r < 0.3:  # 30% chance full glitch char
                                display_ch = random.choice("@#░▒▓ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                            else:  # 70% chance just flicker color
                                display_ch = ch
                            color_attr = random.choice([
                                curses_colors.ansi_0m32, curses_colors.ansi_1m32,
                                curses_colors.ansi_0m36, curses_colors.ansi_1m36,
                                curses_colors.ansi_0m31, curses_colors.ansi_1m31,
                                curses_colors.ansi_0m33, curses_colors.ansi_1m33,
                                curses_colors.ansi_0m35, curses_colors.ansi_1m35
                            ])
                            stdscr.addch(start_y + i, x_start + idx, display_ch, color_attr)
                    # Draw menu options
                    menu_start_y = start_y + len(title_lines) + self.title_menu_spacing
                    for idx, option in enumerate(self.options):
                        arrow = "→ " if idx == self.selected_index else "  "
                        x = max((w - len(option) - 2) // 2, 0)
                        if idx == self.selected_index:
                            stdscr.addstr(menu_start_y + idx, x, arrow, curses_colors.ansi_1m32)
                            stdscr.addstr(menu_start_y + idx, x + len(arrow), option)
                        else:
                            stdscr.addstr(menu_start_y + idx, x, arrow + option)
                    stdscr.refresh()
                    time.sleep(flash_duration)

                    # Reset to normal green title between flashes
                    stdscr.clear()
                    for i, line in enumerate(title_lines):
                        x_start = max((w - len(line)) // 2, 0)
                        for idx, ch in enumerate(line):
                            stdscr.addch(start_y + i, x_start + idx, ch, curses_colors.ansi_1m32)
                    # Redraw menu
                    menu_start_y = start_y + len(title_lines) + self.title_menu_spacing
                    for idx, option in enumerate(self.options):
                        arrow = "» " if idx == self.selected_index else "  "
                        x = max((w - len(option) - 2) // 2, 0)
                        if idx == self.selected_index:
                            stdscr.addstr(menu_start_y + idx, x, arrow, curses_colors.ansi_1m32)
                            stdscr.addstr(menu_start_y + idx, x + len(arrow), option)
                        else:
                            stdscr.addstr(menu_start_y + idx, x, arrow + option)
                    stdscr.refresh()
                    if flash_idx < flashes_per_burst - 1:
                        time.sleep(flash_pause)  # pause between flashes

                last_flash_time = current_time
                flash_interval = random.uniform(1.0, 2.0)  # next burst

            else:
                # Idle: draw normal green title
                start_y = max(
                    (h - len(title_lines) - len(self.options) - self.title_menu_spacing) // 2 - self.vertical_offset, 0)
                for i, line in enumerate(title_lines):
                    x_start = max((w - len(line)) // 2, 0)
                    for idx, ch in enumerate(line):
                        stdscr.addch(start_y + i, x_start + idx, ch, curses_colors.ansi_1m32)
                menu_start_y = start_y + len(title_lines) + self.title_menu_spacing
                for idx, option in enumerate(self.options):
                    arrow = "» " if idx == self.selected_index else "  "
                    x = max((w - len(option) - 2) // 2, 0)
                    if idx == self.selected_index:
                        stdscr.addstr(menu_start_y + idx, x, arrow, curses_colors.ansi_1m32)
                        stdscr.addstr(menu_start_y + idx, x + len(arrow), option)
                    else:
                        stdscr.addstr(menu_start_y + idx, x, arrow + option)
                stdscr.refresh()
            
            # small delay to prevent CPU hogging
            time.sleep(0.01)