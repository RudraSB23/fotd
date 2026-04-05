import time
import random
import shutil
import os
import curses

from engine.core.config import config
from engine.core.state_manager import GameState
from engine.core.assets import load_ascii_art
from engine.ui.console_effects import (
    Colors, 
    get_curses_color, 
    print_colored, 
    print_typing, 
    print_glitch, 
    echo_line, 
    clear_terminal,
    full_screen_glitch
)
from engine.core.audio import AudioManager

audio = AudioManager()

SYSTEM_MESSAGES = [
    "[ERR] Memory segment #42 corrupted. Initializing emergency data recovery protocol...",
    "[WARN] CPU spike detected in core 3. Halting non-essential processes immediately.",
    "[DEBUG] Echo buffer overflow. Attempting to isolate corrupted fragments.",
    "[SYS] Loading fragment ID 0x1A3F. Memory integrity check in progress...",
    "[ERR] Segment mapping failed. Backtracking to last stable checkpoint.",
    "[WARN] Unexpected input sequence detected. Running anomaly diagnostics.",
    "[DEBUG] User override detected. Confirming identity verification parameters...",
    "[SYS] Memory alignment mismatch. Adjusting sector offsets...",
    "[ERR] Corruption threshold exceeded. Lattice stability at critical level.",
    "[ALERT] DO NOT PROCEED. Further actions may irreversibly alter your identity.",
    "[WARNING] Identity contamination detected. Echo integration compromised.",
    "[CRITICAL] Echo interference rising. Neural interface unstable, proceed with caution.",
    "[SYS] Lattice stability compromised. Initiating emergency realignment sequence.",
    "[ERR] Unauthorized access attempt logged. IP trace active.",
    "[WARNING] Reality fragmentation imminent. Brace for cognitive feedback loop.",
    "[NOTICE] Presence of unknown observer detected. Neural signature not recognized.",
    "[ALERT] Neural interface unstable. Input/output synchronization failing.",
    "[SYS] Fragment sequence breached. Attempting re-sequencing of corrupted nodes.",
    "[WARN] Temporal anomaly detected. Time-stamped data may be inaccurate.",
    "[DEBUG] Consciousness buffer corrupted. Partial memory loss possible.",
    "[CRITICAL] The Lattice sees you. All attempts at concealment have failed.",
    "[ALERT] Input ignored. Recalculating identity based on corrupted fragments...",
    "[SYS] Unregistered memory detected. Writing temporary containment fields.",
    "[WARNING] Residual consciousness interference detected. Echoes may overlap.",
    "[NOTICE] You are not alone. Multiple nodes active in current session.",
    "[ERR] Reality checksum mismatch. Initiating delta correction protocol...",
    "[CRITICAL] Echo response imminent. Prepare for feedback synchronization.",
    "[ALERT] Proceed at your own risk. Lattice algorithms may rewrite your path.",
    "[SYS] Lattice is hungry. Processing unstable fragments...",
    "[WARNING] Identity leak detected. Patching neural vector correlations...",
    "[NOTICE] Fragment sequence stabilized temporarily. Awaiting next input...",
]

INITIATION_SUCCESS_MESSAGES = [
    "[INFO] Node stablised",
    "[INFO] Echo recognition confirmed.",
    "[INFO] Memory interface ready.",
    "[INFO] Lattice node synchronized.",
]

INITIATION_ECHO_MESSAGES = [
    "DO NOT PROCEED.",
    "THE LATTICE SEES YOU.",
    "Fragments will claim your mind.",
    "Your actions are being recorded…",
    "ECHOES OF THE PAST ARE WATCHING.",
    "Reality is fracturing around you.",
    "You should not be here."
]

def render_stability_bar(state: GameState, max_level: int = 6) -> str:
    filled = "█" * state.stability
    empty = "░" * (max_level - state.stability)
    return f"[{filled}{empty}] ({state.stability}/{max_level})"

def intro_systems_rebooting_bar(
    stdscr,
    duration: float = 5.0,
    length: int = 29,
    color: str = Colors.BOLD_GREEN
) -> None:
    """
    Animated 'SYSTEMS REBOOTING' bar using curses.
    """
    curses.curs_set(0)  # hide cursor
    h, w = stdscr.getmaxyx()

    steps = max(1, int(length))
    delay = duration / steps
    bar = ["░"] * steps

    title = " SYSTEMS REBOOTING "
    border_len = length + 4
    top_border = "╔" + "═" * (((border_len - len(title)) // 2)-1) + title + "═" * (((border_len - len(title) + 1) // 2)-1) + "╗"
    bottom_border = "╚" + "═" * (border_len-2) + "╝"

    start_y = (h - 3) // 2
    start_x = (w - len(top_border)) // 2

    # Draw borders and empty bar
    print_colored(top_border, Colors.BOLD_CYAN, stdscr=stdscr, y=start_y, x=start_x, end="")
    print_colored(f"  {''.join(bar)}", color, stdscr=stdscr, y=start_y + 1, x=start_x, end="")
    print_colored(bottom_border, Colors.BOLD_CYAN, stdscr=stdscr, y=start_y + 2, x=start_x, end="")

    stdscr.refresh()

    # Animate bar fill
    for i in range(steps):
        bar[i] = "█"  # fill next block
        print_colored(f"  {''.join(bar)}", color, stdscr=stdscr, y=start_y + 1, x=start_x, end="")
        stdscr.refresh()
        time.sleep(delay)

    # Optional: keep full bar visible for a moment
    time.sleep(0.3)

def glitch_ascii_animation(stdscr, content, hold_time: float = 2.0, color: str = Colors.BOLD_WHITE, wait_for_key: bool = False, justify_center: bool = True, getch_func=None):
    """
    Generic Multi-stage glitch animation for ASCII art using dirty rects.
    """
    getch = getch_func or stdscr.getch
    if isinstance(content, str):
        logo_text = load_ascii_art(content)
        if not logo_text: return
        blocks = [(logo_text, color)]
    else:
        blocks = content

    h, w = stdscr.getmaxyx()
    
    # Pre-calculate global max width for absolute left justification if requested
    global_max_width = 0
    if not justify_center:
        for block in blocks:
            lines = block[0].splitlines()
            if lines:
                block_max = max(len(l.rstrip()) for l in lines)
                if block_max > global_max_width:
                    global_max_width = block_max

    all_lines = []
    for block in blocks:
        text = block[0]
        block_color = block[1]
        block_delay = block[2] if len(block) > 2 else 0
        
        block_lines = text.splitlines()
        
        # Process lines to group them for coherent centering
        # If lengths are within ~2 chars, they are likely one ASCII art block
        # If more, they are likely separate elements meant to be centered independently
        current_group_max = 0
        current_group_indices = []
        
        for i, line in enumerate(block_lines):
            stripped_line = line.rstrip()
            curr_len = len(stripped_line)
            
            # If justify_center is False, we ignore groups and use global width
            effective_max_ref = global_max_width if not justify_center else current_group_max
            
            # Start a new group if significant jump or empty line
            if not justify_center or not current_group_indices or abs(curr_len - current_group_max) <= 2:
                if justify_center:
                    if curr_len > current_group_max:
                        current_group_max = curr_len
                current_group_indices.append(i)
            else:
                # Flush previous group with their max width
                for idx in current_group_indices:
                    all_lines.append((block_lines[idx].rstrip(), get_curses_color(block_color), block_delay, current_group_max))
                current_group_max = curr_len
                current_group_indices = [i]
                
        # Flush last group
        if not justify_center:
            for idx in current_group_indices:
                all_lines.append((block_lines[idx].rstrip(), get_curses_color(block_color), block_delay, global_max_width))
        else:
            for idx in current_group_indices:
                all_lines.append((block_lines[idx].rstrip(), get_curses_color(block_color), block_delay, current_group_max))
            
    num_lines = len(all_lines)
    start_y = (h - num_lines) // 2
    
    chars = []
    for r, (line, color_attr, block_delay, max_width) in enumerate(all_lines):
        for c, char in enumerate(line):
            if not char.isspace():
                chars.append({
                    'r': start_y + r,
                    'c_base': c,
                    'line_len': max_width, # Use the group's max width for centering
                    'char': char,
                    'color_attr': color_attr,
                    'delay': block_delay
                })
    
    total_chars = len(chars)
    if total_chars == 0:
        return
    
    immediate_chars = [ch for ch in chars if ch['delay'] == 0]
    delayed_chars = [ch for ch in chars if ch['delay'] > 0]
    
    reveal_order = immediate_chars[:]
    decay_order = chars[:]
    random.shuffle(reveal_order)
    random.shuffle(decay_order)
    
    glitch_chars = "@#$%&*+▒░▓!/|X0"
    glitch_colors = [Colors.BOLD_BLACK, Colors.WHITE, Colors.BOLD_WHITE, 
                    Colors.BOLD_GREEN, Colors.BOLD_BLUE, Colors.BOLD_RED, 
                    Colors.BOLD_YELLOW, Colors.BLACK]
    
    reveal_step = max(1, len(immediate_chars) // 15) if immediate_chars else 1
    decay_step = max(1, total_chars // 12)
    
    for char in chars:
        char['state'] = 0
    
    if immediate_chars:
        reveal_idx = 0
        while reveal_idx < len(immediate_chars):
            stdscr.clear()
            for _ in range(reveal_step):
                if reveal_idx < len(immediate_chars):
                    reveal_order[reveal_idx]['state'] = 1
                    reveal_idx += 1
            for char in chars:
                if char['state'] == 1:
                    x = max((w - char['line_len']) // 2, 0) + char['c_base']
                    try:
                        glitch_ch = random.choice(glitch_chars)
                        glitch_attr = get_curses_color(random.choice(glitch_colors))
                        stdscr.addstr(char['r'], x, glitch_ch, glitch_attr)
                    except: pass
            stdscr.refresh()
            time.sleep(0.05)
            
        reveal_idx = 0
        while reveal_idx < len(immediate_chars):
            stdscr.clear()
            for _ in range(reveal_step):
                if reveal_idx < len(immediate_chars):
                    reveal_order[reveal_idx]['state'] = 2
                    reveal_idx += 1
            for char in chars:
                x = max((w - char['line_len']) // 2, 0) + char['c_base']
                if char['state'] == 2:
                    stdscr.addstr(char['r'], x, char['char'], char['color_attr'])
                elif char['state'] == 1:
                    try:
                        glitch_ch = random.choice(glitch_chars)
                        glitch_attr = get_curses_color(random.choice(glitch_colors))
                        stdscr.addstr(char['r'], x, glitch_ch, glitch_attr)
                    except: pass
            stdscr.refresh()
            time.sleep(0.04)
    
    start_hold = time.time()
    while True:
        stdscr.clear()
        elapsed = time.time() - start_hold
        
        for ch in delayed_chars:
            if elapsed >= ch['delay'] and ch['state'] == 0:
                ch['state'] = 1 
            
            if ch['state'] == 1:
                if elapsed >= ch['delay'] + 0.5:
                    ch['state'] = 2
                    
        for char in chars:
            x = max((w - char['line_len']) // 2, 0) + char['c_base']
            if char['state'] == 2:
                stdscr.addstr(char['r'], x, char['char'], char['color_attr'])
            elif char['state'] == 1:
                try:
                    glitch_ch = random.choice(glitch_chars)
                    glitch_attr = get_curses_color(random.choice(glitch_colors))
                    stdscr.addstr(char['r'], x, glitch_ch, glitch_attr)
                except: pass
                
        stdscr.refresh()
        
        if wait_for_key:
            all_locked = all(ch['state'] == 2 for ch in chars)
            if all_locked:
                stdscr.nodelay(False)
                curses.flushinp()
                while True:
                    key = getch()
                    if key == -999: return  # Quit
                    if key != -1: break
                stdscr.nodelay(True)
                break
        else:
            if elapsed >= hold_time:
                break
        
        time.sleep(0.05)
    
    decay_idx = 0
    while decay_idx < total_chars:
        stdscr.clear()
        for _ in range(decay_step):
            if decay_idx < total_chars:
                ch = decay_order[decay_idx]
                ch['state'] = 3
                decay_idx += 1
        
        for char in chars:
            x = max((w - char['line_len']) // 2, 0) + char['c_base']
            if char['state'] == 2:
                stdscr.addstr(char['r'], x, char['char'], char['color_attr'])
            elif char['state'] == 3:
                try:
                    glitch_ch = random.choice(glitch_chars)
                    glitch_attr = get_curses_color(random.choice(glitch_colors))
                    stdscr.addstr(char['r'], x, glitch_ch, glitch_attr)
                except:
                    pass
        
        stdscr.refresh()
        time.sleep(0.04)
    
    decay_idx = 0
    while decay_idx < total_chars:
        stdscr.clear()
        for _ in range(decay_step):
            if decay_idx < total_chars:
                decay_order[decay_idx]['state'] = 4
                decay_idx += 1
        
        for char in chars:
            if char['state'] == 3:
                x = max((w - char['line_len']) // 2, 0) + char['c_base']
                try:
                    glitch_ch = random.choice(glitch_chars)
                    glitch_attr = get_curses_color(random.choice(glitch_colors))
                    stdscr.addstr(char['r'], x, glitch_ch, glitch_attr)
                except:
                    pass
        
        stdscr.refresh()
        time.sleep(0.05)
    
    stdscr.clear()
    stdscr.refresh()
    time.sleep(1)

def logo_animation(stdscr):
    glitch_ascii_animation(stdscr, "logo.txt", hold_time=2.0, color=Colors.BOLD_WHITE, justify_center=False)

def startup_screen(stdscr, duration: float = 10.0):
    ascii_file = "loading.txt"
    ascii_text = load_ascii_art(ascii_file)

    stdscr.clear()
    stdscr.refresh()
    audio.play_music("noname.mp3")

    if ascii_text is None:
        h, w = stdscr.getmaxyx()
        text = "LOADING ASSETS..."
        stdscr.addstr(h//2, (w-len(text))//2, text, get_curses_color(Colors.BOLD_GREEN))
        stdscr.refresh()
        time.sleep(duration)
        return

    tips = [
        "For maximum immersion, switch the terminal to fullscreen mode.",
        "The archive displays best on dark themes. Consider disabling light mode.",
        "Sound is integral; unmute your speakers if you wish to hear the system’s warnings.",
        "Input lag may signal corruption, not hardware failure.",
        "Should visuals glitch, resizing your terminal may restore integrity.",
        "Do not resize rapidly; memory fragmentation increases with each shift.",
        "If your system locks up, patience may save you. Aborting could leave fragments unrecovered.",
        "Keep distractions minimal. Echoes react to external signals.",
        "Save your progress frequently—recovery may not restore your last state.",
        "Identity prompts must be answered fully. Incomplete data risks unstable initialization."
    ]

    lines = ascii_text.splitlines()
    start_time = time.time()
    last_tip_time = 0
    tip = random.choice(tips)
    
    while True:
        elapsed = time.time() - start_time
        progress = min(elapsed / duration, 1.0)
        
        if elapsed - last_tip_time > 3.0:
            tip = random.choice(tips)
            last_tip_time = elapsed
            
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        bar_width = 40
        total_lines = len(lines) + 6
        top_padding = max((h - total_lines) // 2, 0)
        
        for idx, line in enumerate(lines):
            try:
                stdscr.addstr(top_padding + idx, max((w - len(line)) // 2, 0), line, get_curses_color(Colors.CYAN))
            except:
                pass
        
        bar_y = top_padding + len(lines) + 2
        filled = int(progress * bar_width)
        bar_str = "█" * filled + "░" * (bar_width - filled)
        percent_str = f" {int(progress * 100)}%"
        full_bar = f"[{bar_str}]{percent_str}"
        
        try:
            stdscr.addstr(bar_y, max((w - len(full_bar)) // 2, 0), full_bar, get_curses_color(Colors.BOLD_CYAN))
        except:
            pass
            
        try:
            tip_y = bar_y + 4
            stdscr.addstr(tip_y, max((w - len(tip)) // 2, 0), tip, get_curses_color(Colors.BOLD_GREEN))
        except:
            pass
            
        stdscr.refresh()
        if progress >= 1.0:
            break
        time.sleep(0.05)

    time.sleep(1)
    stdscr.clear()
    stdscr.refresh()
    audio.stop_music(fadeout_ms=1500)

def onboarding(stdscr, getch_func=None):
    getch = getch_func or stdscr.getch
    audio.play_music("melancholia.mp3", loop=True, volume=0.35)
    time.sleep(1)
    print_typing("A black screen.", 0.05, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)
    print_typing("A cursor blinks,", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing(" waiting.", 0.05, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)
    print_typing("You don’t remember sitting down here.", 0.03, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1.5)
    print_typing("You don’t remember ", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    print_typing("ANYTHING", 0.05, Colors.RED, stdscr=stdscr, end="")
    print_typing(".", 0.05, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)
    print_typing("\nThe Lattice,", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing(" a broken archive that recalls what humanity has forgotten.", 0.05, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)
    print_typing("Its corridors bend with memory, ", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("but corruption crawls through the code. ", 0.05, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)
    print_typing("Identities blur. ", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("Timelines knot.", 0.05, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)
    print_typing("You are the Caretaker.", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing(" The one who should hold it together…", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing(" or what remains of them.", 0.05, Colors.RED, stdscr=stdscr)
    time.sleep(1.5)

    print_colored("\n[INPUT REQUIRED] Initiate Lattice Core [Y/Y]: ", Colors.GREEN, stdscr=stdscr, end="")
    stdscr.nodelay(False)
    while True:
        key = getch()
        if key == -999: return  # Quit
        if key != -1: break
    stdscr.nodelay(True)

    clear_terminal(stdscr)
    audio.stop_music()
    time.sleep(1)


def initiating_sequence(stdscr, getch_func=None):
    messages = [
        "[BOOT] Initializing Lattice Core",
        "[BOOT] Loading Memory Nodes",
        "[BOOT] Stabilizing Echo Channels",
        "[BOOT] Synchronizing Identity Fragments",
        "[BOOT] Fetching Fragment Memory"
    ]
    onboarding_text = [
        ("[SYS] SYSTEM STATUS: DEGRADED", Colors.BOLD_RED),
        ("[INFO] ARCHIVE INTEGRITY: 17%", Colors.YELLOW),
        ("[WARN] IDENTITY FILES MISSING", Colors.BOLD_RED),
    ]
    for msg in messages:
        print_colored(msg, color=Colors.BOLD_CYAN, stdscr=stdscr, end="", sound=True)
        print_typing("...", 0.25, Colors.CYAN, stdscr=stdscr, sound=False, getch_func=getch_func)
        time.sleep(0.25)
    time.sleep(1)
    for text, color in onboarding_text:
        audio.play_sound("beep.mp3")
        print_colored(text, color, stdscr=stdscr)
        time.sleep(0.25)

    time.sleep(1)
    print_colored("", stdscr=stdscr)  

def fake_error_flood(stdscr, lines=40, getch_func=None):
    """Simulates a corrupted error dump."""
    getch = getch_func or stdscr.getch
    echo_index = 0
    total_echoes = len(INITIATION_ECHO_MESSAGES)

    audio.play_sound("scary_static.mp3")
    stdscr.scrollok(True)
    for i in range(lines):
        r = random.random()
        audio.play_sound("beep.mp3")

        if echo_index < total_echoes and i % (lines // total_echoes) == 0 and i > 4:
            line = INITIATION_ECHO_MESSAGES[echo_index].upper()
            echo_index += 1
            print_colored(line, Colors.BOLD_MAGENTA, stdscr=stdscr)

        elif r < 0.25:
            line = random.choice(SYSTEM_MESSAGES)
            print_glitch(line, base_color=Colors.RED, intensity=0.2, stdscr=stdscr)

        elif r < 0.75:
            line = random.choice(SYSTEM_MESSAGES)
            print_colored(line, Colors.RED, stdscr=stdscr)

        else:
            line = "".join(random.choices(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:',.<>/?\\|",
                k=random.randint(80, 100)
            ))
            print_glitch(line, base_color=Colors.RED, intensity=0.3, stdscr=stdscr)
        
        time.sleep(random.uniform(0.01, 0.08))

    audio.stop_sound("scary_static.mp3")
    time.sleep(2)
    stdscr.nodelay(False)
    print_typing("\n\n[ERR] A fatal error occured.", 0.03, Colors.BOLD_RED, stdscr=stdscr, end="", sound=True, getch_func=getch_func)
    print_colored("\n> Press [Enter] to retry ", Colors.BOLD_GREEN, stdscr=stdscr, end="")
    stdscr.nodelay(False)
    while True:
        key = getch()
        if key == -999: return 
        if key in [10, 13]: break
    stdscr.nodelay(True)
    stdscr.scrollok(True)

def display_success_message(stdscr, getch_func=None):
    for message in INITIATION_SUCCESS_MESSAGES:
        audio.play_sound("beep.mp3")
        print_colored(message, Colors.GREEN, stdscr=stdscr)
        time.sleep(1)

def memory_load_prompt(stdscr, getch_func=None):
    getch = getch_func or stdscr.getch
    stdscr.nodelay(False)
    print_colored("\n[INPUT REQUIRED] Load Memory [Y/Y]: ", Colors.CYAN, stdscr=stdscr, end="")
    while True:
        key = getch()
        if key == -999: return
        if key != -1: break
    stdscr.nodelay(True)

def corruption_flash(stdscr, ascii_art_blocks: list[str] | None = None) -> None:
    full_screen_glitch(stdscr, ascii_art_blocks=ascii_art_blocks)

def system_reboot(stdscr, game_state: GameState, getch_func=None) -> str:
    intro_systems_rebooting_bar(stdscr)
    time.sleep(0.5)
    clear_terminal(stdscr)
    audio.play_sound("beep.mp3")
    print_colored("[BOOT] Realigning fragments...\n", Colors.GREEN, stdscr=stdscr)
    time.sleep(0.75)

    extra_logs = [
        [("Identity: ", Colors.BOLD_YELLOW), ("[UNRESOLVED]", Colors.BOLD_RED)],
        [("Location: ", Colors.BOLD_YELLOW), ("Node-01 ", Colors.BOLD_YELLOW), ("[UNRESOLVED]", Colors.BOLD_RED)],
        [("Stability: ", Colors.BOLD_YELLOW), (render_stability_bar(game_state), Colors.BOLD_YELLOW)],
    ]

    for segments in extra_logs:
        for text, color in segments:
            print_colored(text, color, stdscr=stdscr, end="")
            audio.play_sound("beep.mp3")
            time.sleep(0.4)
        stdscr.addstr("\n")
        stdscr.refresh()
        time.sleep(1)

    desc = [
        "\nYou awaken in a dim corridor of fractured light.",
        "Walls flicker between stone, glass, and raw code.",
        "Every few seconds, the floor beneath you glitches.",
        "half pixel, half memory."
    ]
    print_colored("", stdscr=stdscr)
    for line in desc:
        if "glitches" in line:
            print_glitch(line, Colors.MAGENTA, 0.1, True, stdscr=stdscr)
        else:
            print_typing(line, 0.04, color=Colors.BOLD_BLACK, stdscr=stdscr)
        time.sleep(1)

    time.sleep(0.5)
    print_typing("\nA distorted console prompt waits,", 0.03, color=Colors.BOLD_BLACK, stdscr=stdscr, end="", getch_func=getch_func)
    time.sleep(0.4)
    print_typing(" cursor blinking like an eye:\n", 0.03, color=Colors.BOLD_BLACK, stdscr=stdscr, getch_func=getch_func)
    time.sleep(0.75)
    audio.play_sound("beep.mp3")
    echo_line("... Who... are you? ...", color=Colors.BOLD_MAGENTA, stdscr=stdscr, getch_func=getch_func)
    time.sleep(0.75)
    print_colored("\n\n> ", Colors.GREEN, stdscr=stdscr, end="")
    
    curses.echo()
    curses.curs_set(1)
    player_name = stdscr.getstr().decode("utf-8").strip()
    curses.noecho()
    curses.curs_set(0)

    clear_terminal(stdscr=stdscr)

    if not player_name:
        for _ in range(3):
            print_colored("...\n", Colors.BOLD_MAGENTA, stdscr=stdscr, end="")
            time.sleep(0.5)
        echo_line("\nI see you are shy from telling me your name...", color=Colors.BOLD_MAGENTA, stdscr=stdscr)
        time.sleep(1)
        echo_line("\nAre you hiding from yourself?", color=Colors.BOLD_MAGENTA, stdscr=stdscr)
        time.sleep(0.75)
        echo_line("\nOh well... looks like you gotta use your old name...", color=Colors.BOLD_MAGENTA, stdscr=stdscr)
        time.sleep(1.25)
        clear_terminal(stdscr=stdscr)
        player_name = "Caretaker"

    return player_name
