import curses
import os
import random
import shutil
import time

from engine.core.assets import load_ascii_art
from engine.core.audio import AudioManager
from engine.core.config import config
from engine.core.state_manager import GameState
from engine.ui.console_effects import (
    Colors,
    clear_terminal,
    echo_line,
    full_screen_glitch,
    get_curses_color,
    print_colored,
    print_glitch,
    print_typing,
)

audio = AudioManager()

INITIATION_SUCCESS_MESSAGES = [
    "[INFO] Node stablised",
    "[INFO] Echo recognition confirmed.",
    "[INFO] Memory interface ready.",
    "[INFO] Lattice node synchronized.",
]


def render_stability_bar(state: GameState, max_level: int = 6) -> str:
    filled = "█" * state.stability
    empty = "░" * (max_level - state.stability)
    return f"[{filled}{empty}] ({state.stability}/{max_level})"


def loading_bar(
    stdscr,
    duration: float = 5.0,
    length: int = 29,
    color: str = Colors.BOLD_GREEN,
    title: str = "LOADING",
) -> None:
    """
    Animated loading bar using curses with customizable title.
    """
    curses.curs_set(0)  # hide cursor
    h, w = stdscr.getmaxyx()

    steps = max(1, int(length))
    delay = duration / steps
    bar = ["░"] * steps

    # Format title with spaces on both sides
    formatted_title = f" {title} "
    border_len = length + 4
    top_border = (
        "╔"
        + "═" * (((border_len - len(formatted_title)) // 2) - 1)
        + formatted_title
        + "═" * (((border_len - len(formatted_title) + 1) // 2) - 1)
        + "╗"
    )
    bottom_border = "╚" + "═" * (border_len - 2) + "╝"

    start_y = (h - 3) // 2
    start_x = (w - len(top_border)) // 2

    # Draw borders and empty bar
    print_colored(
        top_border, Colors.BOLD_CYAN, stdscr=stdscr, y=start_y, x=start_x, end=""
    )
    print_colored(
        f"  {''.join(bar)}", color, stdscr=stdscr, y=start_y + 1, x=start_x, end=""
    )
    print_colored(
        bottom_border, Colors.BOLD_CYAN, stdscr=stdscr, y=start_y + 2, x=start_x, end=""
    )

    stdscr.refresh()

    # Animate bar fill
    for i in range(steps):
        bar[i] = "█"  # fill next block
        print_colored(
            f"  {''.join(bar)}", color, stdscr=stdscr, y=start_y + 1, x=start_x, end=""
        )
        stdscr.refresh()
        time.sleep(delay)

    # Optional: keep full bar visible for a moment
    time.sleep(0.3)


def glitch_ascii_animation(
    stdscr,
    content,
    hold_time: float = 2.0,
    color: str = Colors.BOLD_WHITE,
    wait_for_key: bool = False,
    justify_center: bool = True,
    getch_func=None,
):
    """
    Generic Multi-stage glitch animation for ASCII art using dirty rects.
    """
    getch = getch_func or stdscr.getch
    if isinstance(content, str):
        logo_text = load_ascii_art(content)
        if not logo_text:
            return
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
            effective_max_ref = (
                global_max_width if not justify_center else current_group_max
            )

            # Start a new group if significant jump or empty line
            if (
                not justify_center
                or not current_group_indices
                or abs(curr_len - current_group_max) <= 2
            ):
                if justify_center:
                    if curr_len > current_group_max:
                        current_group_max = curr_len
                current_group_indices.append(i)
            else:
                # Flush previous group with their max width
                for idx in current_group_indices:
                    all_lines.append(
                        (
                            block_lines[idx].rstrip(),
                            get_curses_color(block_color),
                            block_delay,
                            current_group_max,
                        )
                    )
                current_group_max = curr_len
                current_group_indices = [i]

        # Flush last group
        if not justify_center:
            for idx in current_group_indices:
                all_lines.append(
                    (
                        block_lines[idx].rstrip(),
                        get_curses_color(block_color),
                        block_delay,
                        global_max_width,
                    )
                )
        else:
            for idx in current_group_indices:
                all_lines.append(
                    (
                        block_lines[idx].rstrip(),
                        get_curses_color(block_color),
                        block_delay,
                        current_group_max,
                    )
                )

    num_lines = len(all_lines)
    start_y = (h - num_lines) // 2

    chars = []
    for r, (line, color_attr, block_delay, max_width) in enumerate(all_lines):
        for c, char in enumerate(line):
            if not char.isspace():
                chars.append(
                    {
                        "r": start_y + r,
                        "c_base": c,
                        "line_len": max_width,  # Use the group's max width for centering
                        "char": char,
                        "color_attr": color_attr,
                        "delay": block_delay,
                    }
                )

    total_chars = len(chars)
    if total_chars == 0:
        return

    immediate_chars = [ch for ch in chars if ch["delay"] == 0]
    delayed_chars = [ch for ch in chars if ch["delay"] > 0]

    reveal_order = immediate_chars[:]
    decay_order = chars[:]
    random.shuffle(reveal_order)
    random.shuffle(decay_order)

    glitch_chars = "@#$%&*+▒░▓!/|X0"
    glitch_colors = [
        Colors.BOLD_BLACK,
        Colors.WHITE,
        Colors.BOLD_WHITE,
        Colors.BOLD_GREEN,
        Colors.BOLD_BLUE,
        Colors.BOLD_RED,
        Colors.BOLD_YELLOW,
        Colors.BLACK,
    ]

    reveal_step = max(1, len(immediate_chars) // 15) if immediate_chars else 1
    decay_step = max(1, total_chars // 12)

    for char in chars:
        char["state"] = 0

    if immediate_chars:
        reveal_idx = 0
        while reveal_idx < len(immediate_chars):
            stdscr.clear()
            for _ in range(reveal_step):
                if reveal_idx < len(immediate_chars):
                    reveal_order[reveal_idx]["state"] = 1
                    reveal_idx += 1
            for char in chars:
                if char["state"] == 1:
                    x = max((w - char["line_len"]) // 2, 0) + char["c_base"]
                    try:
                        glitch_ch = random.choice(glitch_chars)
                        glitch_attr = get_curses_color(random.choice(glitch_colors))
                        stdscr.addstr(char["r"], x, glitch_ch, glitch_attr)
                    except:
                        pass
            stdscr.refresh()
            time.sleep(0.05)

        reveal_idx = 0
        while reveal_idx < len(immediate_chars):
            stdscr.clear()
            for _ in range(reveal_step):
                if reveal_idx < len(immediate_chars):
                    reveal_order[reveal_idx]["state"] = 2
                    reveal_idx += 1
            for char in chars:
                x = max((w - char["line_len"]) // 2, 0) + char["c_base"]
                if char["state"] == 2:
                    stdscr.addstr(char["r"], x, char["char"], char["color_attr"])
                elif char["state"] == 1:
                    try:
                        glitch_ch = random.choice(glitch_chars)
                        glitch_attr = get_curses_color(random.choice(glitch_colors))
                        stdscr.addstr(char["r"], x, glitch_ch, glitch_attr)
                    except:
                        pass
            stdscr.refresh()
            time.sleep(0.04)

    start_hold = time.time()
    while True:
        stdscr.clear()
        elapsed = time.time() - start_hold

        for ch in delayed_chars:
            if elapsed >= ch["delay"] and ch["state"] == 0:
                ch["state"] = 1

            if ch["state"] == 1:
                if elapsed >= ch["delay"] + 0.5:
                    ch["state"] = 2

        for char in chars:
            x = max((w - char["line_len"]) // 2, 0) + char["c_base"]
            if char["state"] == 2:
                stdscr.addstr(char["r"], x, char["char"], char["color_attr"])
            elif char["state"] == 1:
                try:
                    glitch_ch = random.choice(glitch_chars)
                    glitch_attr = get_curses_color(random.choice(glitch_colors))
                    stdscr.addstr(char["r"], x, glitch_ch, glitch_attr)
                except:
                    pass

        stdscr.refresh()

        if wait_for_key:
            all_locked = all(ch["state"] == 2 for ch in chars)
            if all_locked:
                stdscr.nodelay(False)
                curses.flushinp()
                while True:
                    key = getch()
                    if key == -999:
                        return  # Quit
                    if key != -1:
                        break
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
                ch["state"] = 3
                decay_idx += 1

        for char in chars:
            x = max((w - char["line_len"]) // 2, 0) + char["c_base"]
            if char["state"] == 2:
                stdscr.addstr(char["r"], x, char["char"], char["color_attr"])
            elif char["state"] == 3:
                try:
                    glitch_ch = random.choice(glitch_chars)
                    glitch_attr = get_curses_color(random.choice(glitch_colors))
                    stdscr.addstr(char["r"], x, glitch_ch, glitch_attr)
                except:
                    pass

        stdscr.refresh()
        time.sleep(0.04)

    decay_idx = 0
    while decay_idx < total_chars:
        stdscr.clear()
        for _ in range(decay_step):
            if decay_idx < total_chars:
                decay_order[decay_idx]["state"] = 4
                decay_idx += 1

        for char in chars:
            if char["state"] == 3:
                x = max((w - char["line_len"]) // 2, 0) + char["c_base"]
                try:
                    glitch_ch = random.choice(glitch_chars)
                    glitch_attr = get_curses_color(random.choice(glitch_colors))
                    stdscr.addstr(char["r"], x, glitch_ch, glitch_attr)
                except:
                    pass

        stdscr.refresh()
        time.sleep(0.05)

    stdscr.clear()
    stdscr.refresh()
    time.sleep(1)


def logo_animation(stdscr):
    glitch_ascii_animation(
        stdscr, "logo.txt", hold_time=2.0, color=Colors.BOLD_WHITE, justify_center=False
    )


def startup_screen(stdscr, duration: float = 10.0):
    ascii_file = "loading.txt"
    ascii_text = load_ascii_art(ascii_file)

    stdscr.clear()
    stdscr.refresh()
    audio.play_music("noname.mp3")

    if ascii_text is None:
        h, w = stdscr.getmaxyx()
        text = "LOADING ASSETS..."
        stdscr.addstr(
            h // 2, (w - len(text)) // 2, text, get_curses_color(Colors.BOLD_GREEN)
        )
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
        "Identity prompts must be answered fully. Incomplete data risks unstable initialization.",
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
                stdscr.addstr(
                    top_padding + idx,
                    max((w - len(line)) // 2, 0),
                    line,
                    get_curses_color(Colors.CYAN),
                )
            except:
                pass

        bar_y = top_padding + len(lines) + 2
        filled = int(progress * bar_width)
        bar_str = "█" * filled + "░" * (bar_width - filled)
        percent_str = f" {int(progress * 100)}%"
        full_bar = f"[{bar_str}]{percent_str}"

        try:
            stdscr.addstr(
                bar_y,
                max((w - len(full_bar)) // 2, 0),
                full_bar,
                get_curses_color(Colors.BOLD_CYAN),
            )
        except:
            pass

        try:
            tip_y = bar_y + 4
            stdscr.addstr(
                tip_y,
                max((w - len(tip)) // 2, 0),
                tip,
                get_curses_color(Colors.BOLD_GREEN),
            )
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
    print_typing(
        "You don’t remember sitting down here.", 0.03, Colors.BOLD_BLACK, stdscr=stdscr
    )
    time.sleep(1.5)
    print_typing("You don’t remember ", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    print_typing("ANYTHING", 0.05, Colors.RED, stdscr=stdscr, end="")
    print_typing(".", 0.05, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)
    print_typing("\nThe Lattice,", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing(
        " a broken archive that recalls what humanity has forgotten.",
        0.05,
        Colors.BOLD_BLACK,
        stdscr=stdscr,
    )
    time.sleep(1)
    print_typing(
        "Its corridors bend with memory, ",
        0.05,
        Colors.BOLD_BLACK,
        stdscr=stdscr,
        end="",
    )
    time.sleep(0.4)
    print_typing(
        "but corruption crawls through the code. ",
        0.05,
        Colors.BOLD_BLACK,
        stdscr=stdscr,
    )
    time.sleep(1)
    print_typing("Identities blur. ", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("Timelines knot.", 0.05, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)
    print_typing(
        "You are the Caretaker.", 0.05, Colors.BOLD_BLACK, stdscr=stdscr, end=""
    )
    time.sleep(0.5)
    print_typing(
        " The one who should hold it together…",
        0.05,
        Colors.BOLD_BLACK,
        stdscr=stdscr,
        end="",
    )
    time.sleep(0.5)
    print_typing(" or what remains of them.", 0.05, Colors.RED, stdscr=stdscr)
    time.sleep(1.5)

    print_colored(
        "\nInitiate Apex Lattice [ENTER]: ",
        Colors.GREEN,
        stdscr=stdscr,
        end="",
    )
    stdscr.nodelay(False)
    while True:
        key = getch()
        if key == -999:
            return  # Quit
        if key != -1:
            break
    stdscr.nodelay(True)

    clear_terminal(stdscr)
    audio.stop_music()
    time.sleep(1)


def initiating_sequence(stdscr, getch_func=None):
    messages = [
        "[BOOT] Initializing Apex Lattice",
        "[BOOT] Loading Memory Nodes",
        "[BOOT] Stabilizing Echo Channels",
        "[BOOT] Synchronizing Identity Fragments",
        "[BOOT] Fetching Fragment Memory",
    ]
    onboarding_text = [
        ("[SYS] SYSTEM STATUS: DEGRADED", Colors.BOLD_RED),
        ("[INFO] ARCHIVE INTEGRITY: 17%", Colors.YELLOW),
        ("[WARN] IDENTITY FILES MISSING", Colors.BOLD_RED),
    ]
    for msg in messages:
        print_colored(msg, color=Colors.BOLD_CYAN, stdscr=stdscr, end="", sound=True)
        print_typing(
            "...", 0.25, Colors.CYAN, stdscr=stdscr, sound=False, getch_func=getch_func
        )
        time.sleep(0.25)
    time.sleep(1)
    for text, color in onboarding_text:
        audio.play_sound("beep.mp3")
        print_colored(text, color, stdscr=stdscr)
        time.sleep(0.25)

    time.sleep(1)
    print_colored("", stdscr=stdscr)


def display_success_message(stdscr, getch_func=None):
    for message in INITIATION_SUCCESS_MESSAGES:
        audio.play_sound("beep.mp3")
        print_colored(message, Colors.GREEN, stdscr=stdscr)
        time.sleep(1)


def memory_load_prompt(stdscr, getch_func=None):
    getch = getch_func or stdscr.getch
    stdscr.nodelay(False)
    print_colored(
        "\n[INPUT REQUIRED] Load Memory [Y/Y]: ", Colors.CYAN, stdscr=stdscr, end=""
    )
    while True:
        key = getch()
        if key == -999:
            return
        if key != -1:
            break
    stdscr.nodelay(True)


def apex_lattice_boot(stdscr, getch_func=None) -> None:
    from collections import deque

    clear_terminal(stdscr)
    h, w = stdscr.getmaxyx()

    # Load ASCII art
    apex_art = load_ascii_art("apex_lattice.txt") or "APEX LATTICE"
    art_lines = apex_art.splitlines()
    art_width = max(len(l) for l in art_lines)
    art_x = max((w - art_width) // 2, 0)

    # ── Layout constants ──────────────────────────────────────────────
    ART_HEIGHT = len(art_lines)
    ART_GAP = 2  # blank rows between art and log box
    LOG_HEIGHT = 8
    LOG_WIDTH = 58
    LOG_GAP = 2  # blank rows between log box and bar
    BAR_LENGTH = 40
    BAR_ROWS = 3  # top border + bar + bottom border

    # Total height of the entire block
    TOTAL_HEIGHT = ART_HEIGHT + ART_GAP + (LOG_HEIGHT + 2) + LOG_GAP + BAR_ROWS

    # Vertical offset to centre the whole block
    top_offset = max((h - TOTAL_HEIGHT) // 2, 0)

    # Derive each section's Y from the same offset
    art_y = top_offset
    log_y = art_y + ART_HEIGHT + ART_GAP
    bar_y = log_y + LOG_HEIGHT + 2 + LOG_GAP  # +2 for log top/bottom borders

    # Horizontal centre
    log_x = (w - LOG_WIDTH - 4) // 2
    bar_x = (w - BAR_LENGTH - 4) // 2

    # ── Draw ASCII art ────────────────────────────────────────────────
    for i, line in enumerate(art_lines):
        print_colored(
            line, Colors.BOLD_CYAN, stdscr=stdscr, y=art_y + i, x=art_x, end=""
        )

    stdscr.refresh()
    time.sleep(0.3)

    # ── All log messages ──────────────────────────────────────────────
    ALL_LOGS = [
        ("[CORE] Booting APEX LATTICE kernel...", Colors.BOLD_GREEN),
        ("[CORE] Mapping fragmented memory nodes...", Colors.BOLD_GREEN),
        ("[CORE] Initialising echo resonance matrix...", Colors.BOLD_GREEN),
        ("[CORE] Synchronising Lattice node registry...", Colors.BOLD_GREEN),
        ("[INFO] Initialising fragment indexes...", Colors.BOLD_GREEN),
        ("[CORE] Loading identity anchor protocols...", Colors.BOLD_GREEN),
        ("[WARN] Identity anchor integrity: DEGRADED", Colors.BOLD_YELLOW),
        ("[CORE] Attempting anchor stabilisation...", Colors.BOLD_GREEN),
        ("[WARN] Corruption trace detected in sector 0x4F", Colors.BOLD_YELLOW),
        ("[INFO] Neural interface handshake in progress...", Colors.BOLD_GREEN),
        ("[CORE] Memory lattice partitions: MOUNTED", Colors.BOLD_GREEN),
        ("[WARN] Anomalous signal in echo buffer — ignoring", Colors.BOLD_YELLOW),
        ("[INFO] Observer protocol: ACTIVE", Colors.BOLD_GREEN),
        ("[CORE] Stabilising quantum coherence layer...", Colors.BOLD_GREEN),
        ("[ERROR] Sector 0x1A: data irrecoverable", Colors.BOLD_RED),
        ("[CORE] Bypassing corrupted sectors...", Colors.BOLD_GREEN),
        ("[WARN] Recursion depth limit approaching", Colors.BOLD_YELLOW),
        ("[CORE] Echo chamber alignment: COMPLETE", Colors.BOLD_GREEN),
        ("[INFO] User identity: UNVERIFIED", Colors.BOLD_YELLOW),
        ("[CORE] APEX LATTICE ONLINE", Colors.BOLD_GREEN),
    ]

    # ── Draw static log box border ────────────────────────────────────
    log_top = "╔" + "═" * (LOG_WIDTH + 2) + "╗"
    log_blank = "║" + " " * (LOG_WIDTH + 2) + "║"
    log_bottom = "╚" + "═" * (LOG_WIDTH + 2) + "╝"

    print_colored(log_top, Colors.BOLD_CYAN, stdscr=stdscr, y=log_y, x=log_x, end="")
    for i in range(LOG_HEIGHT):
        print_colored(
            log_blank, Colors.BOLD_CYAN, stdscr=stdscr, y=log_y + 1 + i, x=log_x, end=""
        )
    print_colored(
        log_bottom,
        Colors.BOLD_CYAN,
        stdscr=stdscr,
        y=log_y + LOG_HEIGHT + 1,
        x=log_x,
        end="",
    )

    # ── Draw static bar border ────────────────────────────────────────
    bar_label = " INITIALISING "
    bar_border_w = BAR_LENGTH + 4
    bar_top = (
        "╔"
        + "═" * ((bar_border_w - len(bar_label)) // 2 - 1)
        + bar_label
        + "═" * ((bar_border_w - len(bar_label) + 1) // 2 - 1)
        + "╗"
    )
    bar_bottom = "╚" + "═" * (bar_border_w - 2) + "╝"
    bar_empty = ["░"] * BAR_LENGTH

    print_colored(bar_top, Colors.BOLD_CYAN, stdscr=stdscr, y=bar_y, x=bar_x, end="")
    print_colored(
        f"  {''.join(bar_empty)}",
        Colors.BOLD_GREEN,
        stdscr=stdscr,
        y=bar_y + 1,
        x=bar_x,
        end="",
    )
    print_colored(
        bar_bottom, Colors.BOLD_CYAN, stdscr=stdscr, y=bar_y + 2, x=bar_x, end=""
    )

    stdscr.refresh()

    # ── Scrolling log buffer ──────────────────────────────────────────
    log_buffer = deque(maxlen=LOG_HEIGHT)
    total_steps = BAR_LENGTH
    duration = 5.0
    step_delay = duration / total_steps
    log_interval = max(1, total_steps // len(ALL_LOGS))
    log_index = 0

    def redraw_log():
        lines = list(log_buffer)
        for i in range(LOG_HEIGHT):
            blank_row = " " * LOG_WIDTH
            print_colored(
                blank_row,
                Colors.BOLD_GREEN,
                stdscr=stdscr,
                y=log_y + 1 + i,
                x=log_x + 2,
                end="",
            )
            if i < len(lines):
                text, color = lines[i]
                print_colored(
                    text[:LOG_WIDTH],
                    color,
                    stdscr=stdscr,
                    y=log_y + 1 + i,
                    x=log_x + 2,
                    end="",
                )
        stdscr.refresh()

    # ── Main loop: fill bar + emit logs ──────────────────────────────
    for step in range(total_steps):
        if step > 0 and step % log_interval == 0 and log_index < len(ALL_LOGS):
            log_buffer.append(ALL_LOGS[log_index])
            log_index += 1
            redraw_log()

        bar_empty[step] = "█"
        print_colored(
            f"  {''.join(bar_empty)}",
            Colors.BOLD_GREEN,
            stdscr=stdscr,
            y=bar_y + 1,
            x=bar_x,
            end="",
        )
        stdscr.refresh()
        time.sleep(step_delay)

    # Flush remaining logs after bar completes
    while log_index < len(ALL_LOGS):
        log_buffer.append(ALL_LOGS[log_index])
        log_index += 1
        redraw_log()
        time.sleep(0.08)

    time.sleep(0.6)
    clear_terminal(stdscr)
    time.sleep(0.2)


def system_reboot(stdscr, game_state: GameState, getch_func=None) -> str:
    loading_bar(stdscr, title="SYSTEMS REBOOTING")
    time.sleep(0.5)
    clear_terminal(stdscr)
    audio.play_sound("beep.mp3")
    print_colored("[BOOT] Realigning fragments...\n", Colors.GREEN, stdscr=stdscr)
    time.sleep(0.75)

    extra_logs = [
        [("Identity: ", Colors.BOLD_YELLOW), ("[UNRESOLVED]", Colors.BOLD_RED)],
        [
            ("Location: ", Colors.BOLD_YELLOW),
            ("Node-01 ", Colors.BOLD_YELLOW),
            ("[UNRESOLVED]", Colors.BOLD_RED),
        ],
        [
            ("Stability: ", Colors.BOLD_YELLOW),
            (render_stability_bar(game_state), Colors.BOLD_YELLOW),
        ],
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
        "half pixel, half memory.",
    ]
    print_colored("", stdscr=stdscr)
    for line in desc:
        if "glitches" in line:
            print_glitch(line, Colors.MAGENTA, 0.1, True, stdscr=stdscr)
        else:
            print_typing(line, 0.04, color=Colors.BOLD_BLACK, stdscr=stdscr)
        time.sleep(1)

    time.sleep(0.5)
    print_typing(
        "\nA distorted console prompt waits,",
        0.03,
        color=Colors.BOLD_BLACK,
        stdscr=stdscr,
        end="",
        getch_func=getch_func,
    )
    time.sleep(0.4)
    print_typing(
        " cursor blinking like an eye:\n",
        0.03,
        color=Colors.BOLD_BLACK,
        stdscr=stdscr,
        getch_func=getch_func,
    )
    time.sleep(0.75)
    audio.play_sound("beep.mp3")
    echo_line(
        "... Who... are you? ...",
        color=Colors.BOLD_MAGENTA,
        stdscr=stdscr,
        getch_func=getch_func,
    )
    time.sleep(0.75)
    print_colored("\n\n> ", Colors.GREEN, stdscr=stdscr, end="")

    # Skip name input and use default Caretaker name
    player_name = "Caretaker"

    clear_terminal(stdscr=stdscr)

    return player_name
