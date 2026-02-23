import curses
import random
import time
from typing import Union, List

from engine.audio import *
from engine.console_effects import Colors, CursesColors, print_colored

audio = AudioManager()

class ChoiceMenu:
    def __init__(self, prompt: str, choices: list[str], corruption: int = 0):
        self.prompt = prompt
        self.choices = choices
        self.selected_index = 0
        self.corruption = corruption  # pass current corruption level in!

    def display(self, stdscr) -> int:
        if not self.choices:
            raise ValueError("No choices provided for ChoiceMenu.")
        
        # Setup curses for menu interaction
        curses.curs_set(0)
        stdscr.keypad(True)
        stdscr.nodelay(False)
        curses_colors = CursesColors()
        
        # Get current cursor position to avoid overlapping previous text
        curr_y, curr_x = stdscr.getyx()
        
        # If we are at the bottom of the screen, we might need to scroll or adjust
        # For now, we assume there is enough space or curses handles scrolling
        prompt_lines = self.prompt.splitlines() if self.prompt else []
        
        # We start the menu after the prompt
        menu_start_y = curr_y + len(prompt_lines) + 1
        max_h, max_w = stdscr.getmaxyx()

        arrow_choices = ["→ ", "» ", "▓ ", "█ ", "▒ "]

        while True:
            # Clear menu lines only (not the whole screen)
            for idx in range(len(self.choices)):
                if menu_start_y + idx < max_h:
                    stdscr.move(menu_start_y + idx, 0)
                    stdscr.clrtoeol()

            # Display prompt if provided
            for idx, line in enumerate(prompt_lines):
                if curr_y + idx < max_h:
                    stdscr.addstr(curr_y + idx, 0, line, curses_colors.ansi_1m36)

            # Display choices
            for idx, choice in enumerate(self.choices):
                if menu_start_y + idx < max_h:
                    # CORRUPTION EFFECTS:
                    prefix = "→ " if idx == self.selected_index else "  "
                    
                    if self.corruption >= 5 and idx == self.selected_index and random.random() < 0.2:
                        # Glitchy arrow
                        glitch_arrows = ["→ ", "» ", "▓ ", "█ ", "▒ "]
                        prefix = random.choice(glitch_arrows)
                    
                    # Note: shuffling choices is complex to implement here without changing selection logic
                    # keeping it simple for now as per base requirement.
                    
                    color = curses_colors.ansi_1m32 if idx == self.selected_index else curses.color_pair(0)
                    stdscr.addstr(menu_start_y + idx, 0, prefix, color)
                    stdscr.addstr(menu_start_y + idx, len(prefix), choice)
            
            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP:
                self.selected_index = (self.selected_index - 1) % len(self.choices)
            elif key == curses.KEY_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.choices)
            elif key in [10, 13]:
                audio.play_sound(random.choice(["beep.mp3", "static.mp3"]))
                # After selection, move cursor to the line after the menu
                final_y = min(max_h - 1, menu_start_y + len(self.choices))
                stdscr.move(final_y, 0)
                return self.selected_index

class TimedPuzzle:
    def __init__(self, target_word: str, difficulty: int = 1, time_limit: float = 10.0, auto_start: bool = False, game_state=None):
        self.target_word = target_word.upper()
        self.difficulty = difficulty
        self.game_state = game_state
        bonus_time = game_state.stability // 4 if game_state else 0  # +2s at stability 8
        self.time_limit = time_limit + bonus_time
        self.auto_start = auto_start
        self.scrambled_word = self._scramble(self.target_word, difficulty)
        self.input_text = ""

    def _scramble(self, word: str, difficulty: int) -> str:
        leetspeak = {
            "a": "@", "A": "Λ", "b": "8", "B": "8", "c": "(", "C": "©",
            "d": "Ð", "D": "Ð", "e": "3", "E": "3", "f": "ƒ", "F": "ƒ",
            "g": "9", "G": "9", "h": "#", "H": "#", "i": "1", "I": "!",
            "j": "]", "J": "]", "k": "X", "K": "×", "l": "1", "L": "|",
            "m": "^^", "M": "^^", "n": "Ñ", "N": "Ñ", "o": "0", "O": "0",
            "p": "¶", "P": "¶", "q": "9", "Q": "9", "r": "®", "R": "®",
            "s": "$", "S": "$", "t": "+", "T": "+", "u": "µ", "U": "µ",
            "v": "√", "V": "√", "w": "ω", "W": "WW", "x": "×", "X": "×",
            "y": "¥", "Y": "¥", "z": "2", "Z": "2"
        }

        chars = list(word)
        if not chars: return ""
        
        # 1. Leetspeak Layer: Probability scales with difficulty
        # Difficulty 1 = 20%, Difficulty 5 = 100%
        leet_prob = min(0.2 * difficulty, 1.0)
        for i in range(len(chars)):
            if chars[i] in leetspeak and random.random() < leet_prob:
                chars[i] = leetspeak[chars[i]]
        
        # 2. Character Swaps: Number of swaps scales with difficulty
        # Only starts at difficulty 2
        num_swaps = max(0, difficulty - 1)
        for _ in range(num_swaps):
            if len(chars) >= 2:
                idx1, idx2 = random.sample(range(len(chars)), 2)
                chars[idx1], chars[idx2] = chars[idx2], chars[idx1]
        
        # 3. Heavy Symbol Corruption: Probability scales with difficulty
        # Only starts at difficulty 3
        if difficulty >= 3:
            # Difficulty 3 = 10%, Difficulty 5 = 30%
            symbol_prob = min(0.1 * (difficulty - 2), 0.5)
            symbols = ["@", "#", "$", "%", "&", "!", "?", "▓", "▒", "░", "×"]
            for i in range(len(chars)):
                if random.random() < symbol_prob:
                    chars[i] = random.choice(symbols)
                
        return "".join(chars)

    def display(self, stdscr) -> bool:
        from engine.console_effects import clear_terminal, print_centered
        
        # 1. Initialization and Layout Setup
        clear_terminal(stdscr)
        curses.curs_set(0) # Hide cursor initially
        max_h, max_w = stdscr.getmaxyx()
        
        # Calculate Box Dimensions once for all states
        puzzle_headers = [
            "STABILIZE NODE:",
            f"[ {self.scrambled_word} ]",
            f"TIME REMAINING: 10.0s",
            f"> " + " " * 24, # Allocation for typical user input length
            "[ PRESS ENTER TO STABILIZE ]"
        ]
        box_width = max(len(h) for h in puzzle_headers) + 8
        box_height = 10
        
        start_y = (max_h - box_height) // 2
        start_x = (max_w - box_width) // 2
        
        # 2. Internal wait logic if auto_start is False
        if not self.auto_start:
            stdscr.nodelay(False)
            while True:
                # Draw Border using centralized logic
                MessageBox.draw_box(stdscr, start_y, start_x, box_width, box_height, Colors.BOLD_MAGENTA)
                
                # Render ONLY the prompt internally
                prompt = "[ PRESS ENTER TO STABILIZE ]"
                p_x = start_x + (box_width - len(prompt)) // 2
                print_colored(prompt, Colors.BOLD_RED, stdscr=stdscr, y=start_y + (box_height // 2), x=p_x, end="")
                stdscr.refresh()
                
                key = stdscr.getch()
                if key in [10, 13]:
                    break
            clear_terminal(stdscr)
        
        # 3. Active Puzzle Execution
        stdscr.nodelay(True)
        start_time = time.time()
        success = False
        current_border_color = Colors.BOLD_MAGENTA
        
        while True:
            elapsed = time.time() - start_time
            remaining = max(0, self.time_limit - elapsed)
            
            # Check for Timeout
            if remaining <= 0:
                success = False
                current_border_color = Colors.BOLD_RED
                break
                
            # Check for Success
            if self.input_text.upper() == self.target_word.upper():
                success = True
                current_border_color = Colors.BOLD_GREEN
                break
            
            # Draw Box using centralized logic with subtle corruption glitch
            MessageBox.draw_box(stdscr, start_y, start_x, box_width, box_height, current_border_color, glitch_prob=0.02)

            # Display Content with mathematical centering
            title_str = "STABILIZE NODE:"
            title_x = start_x + (box_width - len(title_str)) // 2
            print_colored(title_str, Colors.BOLD_MAGENTA, stdscr=stdscr, y=start_y + 1, x=title_x, end="")
            
            scrambled_str = f"[ {self.scrambled_word} ]"
            s_x = start_x + (box_width - len(scrambled_str)) // 2
            print_colored(scrambled_str, Colors.BOLD_MAGENTA, stdscr=stdscr, y=start_y + 3, x=s_x, end="")
            
            timer_str = f"TIME REMAINING: {remaining:.1f}s"
            t_x = start_x + (box_width - len(timer_str)) // 2
            timer_color = Colors.BOLD_RED if remaining < 3 else Colors.BOLD_YELLOW
            print_colored(timer_str, timer_color, stdscr=stdscr, y=start_y + 5, x=t_x, end="")
            
            # Input Rendering with proper centering
            input_display = f"> {self.input_text}"
            if len(input_display) > box_width - 8:
                input_display = "> ..." + input_display[-(box_width - 12):]
            i_x = start_x + (box_width - len(input_display)) // 2
            print_colored(input_display, Colors.BOLD_GREEN, stdscr=stdscr, y=start_y + 7, x=i_x, end="")
            
            stdscr.refresh()
            
            # Input Handling
            try:
                key = stdscr.getch()
                if key != -1 and key != 27:  # ignore ESC
                    if key in [8, 127, curses.KEY_BACKSPACE]:
                        self.input_text = self.input_text[:-1]
                    elif 32 <= key <= 126:
                        self.input_text += chr(key)
            except:
                pass
            
            time.sleep(0.01)

        # 4. Final Feedback Rendering
        if not success:
            # Full-screen glitch flash on failure
            from engine.console_effects import full_screen_glitch
            audio.play_sound("glitch.mp3")
            full_screen_glitch(stdscr, frames=60, frame_delay=0.02)
            audio.stop_sound("glitch.mp3")
            
            # High-intensity failure glitch loop
            fail_start = time.time()
            audio.play_sound("fail.mp3")
            while time.time() - fail_start < 1.0:
                stdscr.clear()
                MessageBox.draw_box(stdscr, start_y, start_x, box_width, box_height, Colors.BOLD_RED, glitch_prob=0.35)
                
                # Glitchy failure message
                msg_lines = ["STABILIZATION", "FAILED"]
                for i, line in enumerate(msg_lines):
                    glitch_line = "".join(random.choice("@#░▒▓$!%?&") if random.random() < 0.2 else c for c in line)
                    f_x = start_x + (box_width - len(glitch_line)) // 2
                    f_y = start_y + (box_height // 2) - 1 + i
                    print_colored(glitch_line, random.choice([Colors.BOLD_RED, Colors.BOLD_WHITE]), stdscr=stdscr, y=f_y, x=f_x, end="")
                
                stdscr.refresh()
                time.sleep(0.05)
        else:
            audio.play_sound("success.mp3")

        # Redraw box with final result color using centralized logic
        MessageBox.draw_box(stdscr, start_y, start_x, box_width, box_height, current_border_color)

        msg_lines = ["STABILIZATION", "COMPLETE" if success else "FAILED"]
        final_color = Colors.BOLD_GREEN if success else Colors.BOLD_RED
        
        # Center final result across two lines
        mid_y = start_y + (box_height // 2)
        for i, line in enumerate(msg_lines):
            f_x = start_x + (box_width - len(line)) // 2
            f_y = mid_y - 1 + i
            print_colored(line, final_color, stdscr=stdscr, y=f_y, x=f_x, end="")
        stdscr.refresh()

        time.sleep(1.5)
        
        # Cleanup
        stdscr.nodelay(False)
        clear_terminal(stdscr)
        return success

class MessageBox:
    @staticmethod
    def draw_box(stdscr, y, x, width, height, color, glitch_prob: float = 0.0):
        # Local imports to avoid circular deps if they occur
        glitch_chars = "@#░▒▓$!%?&"
        
        for i in range(height):
            if i == 0:
                text = "╔" + "═" * (width - 2) + "╗"
            elif i == height - 1:
                text = "╚" + "═" * (width - 2) + "╝"
            else:
                text = "║" + " " * (width - 2) + "║"

            # Render with optional glitching
            for idx, ch in enumerate(text):
                char_to_draw = ch
                draw_color = color
                
                if glitch_prob > 0 and random.random() < glitch_prob:
                    char_to_draw = random.choice(glitch_chars)
                    draw_color = random.choice([
                        Colors.BOLD_RED, Colors.BOLD_YELLOW, Colors.BOLD_MAGENTA, 
                        Colors.BOLD_CYAN, Colors.BOLD_WHITE
                    ])
                
                print_colored(char_to_draw, draw_color, stdscr=stdscr, y=y + i, x=x + idx, end="")
    def __init__(self, 
                 message: Union[str, List[str]], 
                 title: str = None, 
                 choices: List[str] = None, 
                 border_color: str = Colors.BOLD_CYAN,
                 text_color: str = Colors.RESET):
        self.message = [message] if isinstance(message, str) else message
        self.title = title
        self.choices = choices
        self.border_color = border_color
        self.text_color = text_color
        self.selected_index = 0

    def display(self, stdscr, duration: float = None) -> Union[None, int]:
        curses.curs_set(0)
        stdscr.keypad(True)
        stdscr.nodelay(False)
        
        max_h, max_w = stdscr.getmaxyx()
        
        # Helper to get visual length of a message line
        def get_line_len(line):
            if isinstance(line, str):
                return len(line)
            if isinstance(line, tuple):
                return len(line[0])
            if isinstance(line, list):
                return sum(len(segment[0] if isinstance(segment, tuple) else segment) for segment in line)
            return 0

        # Calculate dimensions
        content_width = max(get_line_len(line) for line in self.message)
        if self.title:
            content_width = max(content_width, len(self.title) + 4)
        if self.choices:
            choice_width = max(len(c) + 4 for c in self.choices)
            content_width = max(content_width, choice_width)
            
        box_width = min(content_width + 8, max_w - 4)
        box_height = len(self.message) + 4
        if self.title: box_height += 1
        if self.choices: box_height += len(self.choices) + 1
        
        start_y = (max_h - box_height) // 2
        start_x = (max_w - box_width) // 2
        
        while True:
            # Draw Border using centralized logic
            self.draw_box(stdscr, start_y, start_x, box_width, box_height, self.border_color)

            # Draw Title if exists
            current_line_y = start_y + 1
            if self.title:
                title_str = f" {self.title} "
                t_x = start_x + (box_width - len(title_str)) // 2
                print_colored(title_str, self.border_color, stdscr=stdscr, y=start_y, x=t_x, end="")
                current_line_y += 1
            
            # Print Message Lines (Rich Text Support)
            for line in self.message:
                line_len = get_line_len(line)
                m_x = start_x + (box_width - line_len) // 2
                
                if isinstance(line, str):
                    print_colored(line, self.text_color, stdscr=stdscr, y=current_line_y, x=m_x, end="")
                elif isinstance(line, tuple):
                    text, color = line
                    print_colored(text, color, stdscr=stdscr, y=current_line_y, x=m_x, end="")
                elif isinstance(line, list):
                    curr_x = m_x
                    for segment in line:
                        if isinstance(segment, tuple):
                            text, color = segment
                        else:
                            text, color = segment, self.text_color
                        print_colored(text, color, stdscr=stdscr, y=current_line_y, x=curr_x, end="")
                        curr_x += len(text)
                
                current_line_y += 1
            
            # If choices exist
            if self.choices:
                current_line_y += 1
                for idx, choice in enumerate(self.choices):
                    prefix = "→ " if idx == self.selected_index else "  "
                    c_str = f"{prefix}{choice}"
                    c_x = start_x + (box_width - len(c_str)) // 2
                    c_color = Colors.BOLD_GREEN if idx == self.selected_index else self.text_color
                    print_colored(c_str, c_color, stdscr=stdscr, y=current_line_y, x=c_x, end="")
                    current_line_y += 1
                
                stdscr.refresh()
                key = stdscr.getch()
                if key == curses.KEY_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.choices)
                elif key == curses.KEY_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.choices)
                elif key in [10, 13]:
                    audio.play_sound(random.choice(["beep.mp3", "static.mp3"]))
                    from engine.console_effects import clear_terminal
                    clear_terminal(stdscr)
                    return self.selected_index
            else:
                # Info Mode
                stdscr.refresh()
                if duration:
                    time.sleep(duration)
                    from engine.console_effects import clear_terminal
                    clear_terminal(stdscr)
                    return None
                else:
                    stdscr.nodelay(False)
                    stdscr.getch()
                    from engine.console_effects import clear_terminal
                    clear_terminal(stdscr)
                    return None