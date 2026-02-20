import time
import random
import shutil
import os
import getpass

from engine import config
from engine import GameState
from engine.assets import *
from engine.console_effects import *
from engine.audio import AudioManager
from engine.elements import *
from engine.state_manager import *
from engine.save_manager import SaveManager


audio = AudioManager()
game_state = GameState()

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
ECHO_LINES_SCENE1 = [
    "You… are not alone…",
    "Can you hear me?",
    "Every step… closer to yourself… or to me…",
    "Fragments… they are watching…",
    "Do you remember… or imagine…?",
    "Follow… or stop… there is no difference…",
    "I see them… behind the walls… your face… or theirs…",
    "Shadows of memory… fading…",
    "Do you want to be whole… or shattered…?",
    "The corridor bends… you bend…",
    "Listen… they whisper… in the static…",
    "Somebody… someone you were… is still here…",
    "I am… always here… waiting…",
    "You can’t escape… not really…",
    "Stability… slipping… feel it…",
    "You feel tugged… pulled… guided… by me…",
    "All paths… lead to the same echo…",
    "Do you see… your reflection… or mine…?",
    "Fading… breaking… yet alive…",
    "Step forward… step backward… the choice is mine…",
]

ascii_blocks = load_ascii_art("intro_glitch.txt")

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




# ----------------------------------------------------------------------------------------
# GAME SEQUENCE
# ----------------------------------------------------------------------------------------

def startup_screen(duration: float = 5.0):
    ascii_file = "loading.txt"
    ascii_text = load_ascii_art(ascii_file)

    clear_main_terminal()

    audio.play_music("noname.mp3")

    if ascii_text is None:
        normal_print_colored("LOADING ASSETS...\n", ANSIColors.BOLD_GREEN, center=True)
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
    second_last_idx = 4
    last_idx = 5
    dot_states = ["", "██╗", "██╗██╗", "██╗██╗██╗"]
    dot_spacing = ["", "   ", "      ", "         "]
    tip_index = 0
    tip_padding = 1
    start_time = time.time()

    while time.time() - start_time < duration:
        tip = random.choice(tips)

        for dot_state in dot_states:
            os.system("cls" if os.name == "nt" else "clear")

            cols, rows = shutil.get_terminal_size((80, 24))
            dot_padding = dot_spacing[dot_states.index(dot_state)]
            total_lines = len(lines) + 2 + tip_padding
            top_padding = max((rows - total_lines) // 2, 0)
            normal_print_colored("\n" * top_padding)

            # print ascii with dots
            for idx, line in enumerate(lines):
                if idx == second_last_idx:
                    normal_print_colored(f"{line}{dot_state}", color=ANSIColors.CYAN, center=True)
                elif idx == last_idx:
                    dot_bottom = dot_state.replace("██╗", "╚═╝")
                    normal_print_colored(f"{line}{dot_bottom}", color=ANSIColors.CYAN, center=True)
                else:
                    normal_print_colored(f"{line}{dot_padding}", color=ANSIColors.CYAN, center=True)

            print("\n" * tip_padding)
            normal_print_colored(tip, ANSIColors.BOLD_GREEN, center=True)

            time.sleep(0.75)

        tip_index += 1

    clear_main_terminal()
    audio.stop_music(fadeout_ms=1500)


def onboarding(stdscr):
    # colorized items as (text, color) tuples — no inline Colors.* in strings
    onboarding_text = [
        ("[SYS] SYSTEM STATUS: DEGRADED", Colors.BOLD_RED),
        ("[INFO] ARCHIVE INTEGRITY: 17%", Colors.YELLOW),
        ("[WARN] IDENTITY FILES MISSING", Colors.BOLD_RED),
    ]

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
    key = stdscr.getch()
    stdscr.nodelay(True)

    clear_terminal(stdscr)
    audio.stop_music()
    time.sleep(1)

    for text, color in onboarding_text:
        audio.play_sound("beep.mp3")
        print_colored(text, color, stdscr=stdscr)
        time.sleep(round(len(text) / 50) + 0.5)


def initiating_sequence(stdscr):
    messages = [
        "[BOOT] Initializing Lattice Core",
        "[BOOT] Loading Memory Nodes",
        "[BOOT] Stabilizing Echo Channels",
        "[BOOT] Synchronizing Identity Fragments",
        "[BOOT] Fetching Fragment Memory"
    ]
    for msg in messages:
        print_colored(msg, color=Colors.BOLD_CYAN, stdscr=stdscr, end="", sound=True)
        print_typing("...", 0.25, Colors.CYAN, stdscr=stdscr, sound=False)
        time.sleep(0.25)
    time.sleep(1)
    print_colored("", stdscr=stdscr)  

def fake_error_flood(stdscr, lines=40):
    """Simulates a corrupted error dump with mix of gibberish, system messages, and intact scary messages."""
    initiating_sequence_echo_index = 0
    total_echoes = len(INITIATION_ECHO_MESSAGES)

    audio.play_sound("scary_static.mp3")
    stdscr.scrollok(True)
    for i in range(lines):
        r = random.random()
        audio.play_sound("beep.mp3")

        if initiating_sequence_echo_index < total_echoes and i % (lines // total_echoes) == 0 and i > 4:
            line = INITIATION_ECHO_MESSAGES[initiating_sequence_echo_index].upper()
            initiating_sequence_echo_index += 1
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
    print_typing("\n\n[ERR] A fatal error occured.", 0.03, Colors.BOLD_RED, stdscr=stdscr, end="", sound=True)
    print_colored("\n> Press [Enter] to retry: ", Colors.BOLD_GREEN, stdscr=stdscr, end="")
    stdscr.getch()
    stdscr.nodelay(True)
    stdscr.scrollok(True)

def display_success_message(stdscr):
    for message in INITIATION_SUCCESS_MESSAGES:
        audio.play_sound("beep.mp3")
        print_colored(message, Colors.GREEN, stdscr=stdscr)
        time.sleep(1)

def memory_load_prompt(stdscr):
    stdscr.nodelay(False)
    print_colored("\n[INPUT REQUIRED] Load Memory: [Y/Y] ", Colors.CYAN, stdscr=stdscr, end="")
    stdscr.getch()
    stdscr.nodelay(True)

def corruption_flash(stdscr, ascii_art_blocks: list[str] | None = None) -> None:
    from engine.console_effects import full_screen_glitch
    full_screen_glitch(stdscr, ascii_art_blocks=ascii_art_blocks)


def system_reboot(stdscr, game_state) -> str:
    # === 1. Boot Logs ===
    intro_systems_rebooting_bar(stdscr)
    time.sleep(0.5)
    clear_terminal(stdscr)
    audio.play_sound("beep.mp3")
    print_colored("[BOOT] Realigning fragments...\n", Colors.GREEN, stdscr=stdscr)
    time.sleep(0.75)

    # Multi-color messages using tuples; render each segment in order
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

    # === 2. Atmospheric World Description ===
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

    # === 3. First Prompt (Player Name) ===
    print_typing("\nA distorted console prompt waits,", 0.03, color=Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing(" cursor blinking like an eye:\n", 0.03, color=Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)
    audio.play_sound("beep.mp3")
    echo_line("... Who... are you? ...", color=Colors.BOLD_MAGENTA, stdscr=stdscr,)
    time.sleep(0.75)
    print_colored("\n\n> ", Colors.GREEN, stdscr=stdscr, end="")
    
    # Enable visibility for input
    curses.echo()
    curses.curs_set(1)
    
    player_name = stdscr.getstr().decode("utf-8").strip()
    
    # Disable visibility again
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


def scene1_identity_sequence(stdscr, game_state: GameState):
    player_name = game_state.player_name
    SaveManager.save_game(game_state, "scene1_identity_sequence", stdscr=stdscr)
    # === 1. System registering name ===
    audio.play_sound("beep.mp3")
    print_colored(f"\n[SYS] Identity registered: {player_name}", Colors.GREEN, stdscr=stdscr)
    time.sleep(1)
    audio.play_sound("beep.mp3")
    print_colored("[WARN] Memory integrity... FRAGMENTED", Colors.RED, stdscr=stdscr)
    time.sleep(1)

    # === 2. Corridor anomaly ===
    print_colored("", stdscr=stdscr)
    print_typing("The corridor shivers.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing(" Something presses against the walls of code.", 0.04, Colors.BOLD_BLACK,
                 stdscr=stdscr)
    time.sleep(0.75)
    print_typing("A whisper leaks through the static...\n", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)
    clear_terminal(stdscr)

    audio.play_sound("scary_static.mp3", loop=True, volume=1)
    stdscr.scrollok(True)
    for i in range(750):
        print_colored(f"...{player_name}...    ", Colors.RED, stdscr=stdscr, end="")
        time.sleep(0.0025)
    stdscr.scrollok(False)

    audio.stop_sound("scary_static.mp3")
    clear_terminal(stdscr)
    time.sleep(1)

    # === 4. First player choice ===
    print_typing("The corridor stretches endlessly in front of you.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)
    print_typing("The air hums with fractured memory.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)
    menu = ChoiceMenu(
        "\n",
        ["Explore the corridor", "Stand still"],
        game_state.corruption_level
    )
    choice = menu.display(stdscr)

    # === 5. Branching outcome ===
    if choice == 0:
        scene1_corridor_explore(stdscr, game_state)
    elif choice == 1:
        scene1_corridor_stand(stdscr, game_state)

    menu = ChoiceMenu(None, ["Follow the guiding whispers", "Defy the pull and resist"], game_state.corruption_level)
    choice = menu.display(stdscr)

    if choice == 0:  # follow
        echo_line("...yes... deeper... don’t turn back now...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
        game_state.apply_effect("corruption+2")
        return scene1_corridor_part2(stdscr, game_state, path="follow")
    elif choice == 1:  # resist
        echo_line("...no... don’t leave me here...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
        game_state.apply_effect("stability+2")
        return scene1_corridor_part2(stdscr, game_state, path="resist")


def scene1_corridor_explore(stdscr, game_state: GameState):
    SaveManager.save_game(game_state, "scene1_corridor_explore", stdscr=stdscr)
    clear_terminal(stdscr)

    print_typing("You decide to move forward. ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("The corridor's walls ripple like liquid glass as it extends indefinitely.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)

    print_typing("Every step reverberates, ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("not as sound, ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("but as static bursts against your consciousness.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)

    print_typing("Shards of broken code dangle from the ceiling, ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("swinging like icicles, ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("fragments of memories long lost.\n", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)

    echo_line(random.choice(ECHO_LINES_SCENE1), 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
    game_state.apply_effect("corruption+1")
    time.sleep(1)

    print_typing("The deeper you go,", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing(" the further reality warps.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing(" Your reflection in the walls flickers,", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing(" sometimes showing someone else…", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.5)
    print_typing("or ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    print_typing("SOMEONE YOU MIGHT HAVE BEEN.\n", 0.04, Colors.BOLD_RED, stdscr=stdscr)
    time.sleep(1.25)

    echo_line("Every step… closer to yourself… or to me…", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
    game_state.apply_effect("corruption+1")
    time.sleep(1.25)

    audio.play_sound("beep.mp3")
    print_colored("\n[WARN] Stability decreasing... fragments detected.\n", Colors.RED, stdscr=stdscr)
    game_state.apply_effect("stability-1")  # feeling unstable from the corridor
    time.sleep(1)

    print_typing("You feel a faint tug, ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("like an unseen presence guiding you forward, ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("whispering in broken code.\n", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.75)

    echo_line("Fragments... they are watching... Follow... or stop... there is no difference...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
    game_state.apply_effect("corruption+1")
    time.sleep(1.25)

    return True

def scene1_corridor_stand(stdscr, game_state: GameState):
    SaveManager.save_game(game_state, "scene1_corridor_stand", stdscr=stdscr)
    clear_terminal(stdscr)

    print_typing("You stand still. ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("The silence stretches...", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)

    print_typing("The corridor holds its breath with you.\n", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1.2)

    echo_line("> Thank you... I need more time to reach you...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
    game_state.apply_effect("stability+1")
    time.sleep(1.5)

    print_typing("\nA flicker passes along the glass walls. ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("Not corruption this time, ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("but memory.\n", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)

    echo_line("Fragment located... | identity shard detected...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
    game_state.apply_effect("fragment:shard_001")  # add first memory fragment
    time.sleep(1.2)

    print_typing("\nThe walls whisper faintly, ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("as though voices are trying to align themselves into words.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1.25)

    echo_line("\n...don’t forget...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="")
    time.sleep(0.4)
    echo_line(" caretaker...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="")
    time.sleep(0.4)
    echo_line(" you are still here...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr)
    game_state.apply_effect("stability+1")
    time.sleep(1.2)

    print_typing("\n\nThen, as quickly as it came,", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing(" the sensation fades,", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing(" replaced by the cold hum of the corridor.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)

    return True

def scene1_corridor_part2(stdscr, game_state: GameState, path: str):
    clear_terminal(stdscr)
    time.sleep(1)

    if path == "follow":
        print_typing("You surrender to the pull. ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
        time.sleep(0.5)
        print_typing("The corridor stops being a place and begins to feel like a pulse.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
        time.sleep(1.2)
        echo_line("...good... much better... don't you feel the weight lifting?...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr)
        time.sleep(1)
        print_colored("\n[!] DATA OVERFLOW: Narrative streams merging.", Colors.BOLD_RED, stdscr=stdscr)
        game_state.apply_effect("corruption+1")
    else:
        print_typing("You plant your feet and refuse the guiding whispers. ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
        time.sleep(0.5)
        print_typing("The air grows cold, and the walls hum with static protest.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
        time.sleep(1.2)
        echo_line("...obstinate... you always were... persistent...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr)
        time.sleep(1)
        print_colored("\n[#] STABILITY CHECK: Identity tether holding.", Colors.BOLD_CYAN, stdscr=stdscr)
        game_state.apply_effect("stability+1")

    time.sleep(2)
    clear_terminal(stdscr)
    
    # Transition to Node 0x2
    print_colored("<<< EXITING NODE 0x1 >>>\n", Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)
    
    # Simulating a node synchronization bar
    intro_systems_rebooting_bar(stdscr, duration=3.0, color=Colors.BOLD_CYAN)
    clear_terminal(stdscr)
    
    return node0x2_ava_intro(stdscr, game_state)

def node0x2_ava_intro(stdscr, game_state: GameState):
    SaveManager.save_game(game_state, "node0x2_ava_intro", stdscr=stdscr)
    audio.play_sound("beep.mp3")
    print_colored("<<< ENTERING NODE 0x2: FRAGMENT ALPHA >>>\n", Colors.GREEN, stdscr=stdscr)
    time.sleep(1.5)

    print_typing("The scenery shifts. ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("The endless corridor collapses into a single, small room.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(0.8)
    print_typing("There is a flicker in the center—a figure made of data shards.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1.2)

    echo_line("...Ava?...", 0.06, Colors.BOLD_MAGENTA, stdscr=stdscr)
    time.sleep(0.5)
    
    print_typing("\nThe figure stabilizes for a moment. ", 0.04, Colors.BOLD_BLACK, stdscr=stdscr, end="")
    print_typing("She looks at you with eyes that aren't quite aligned.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)

    print_typing("\nIs... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("is someone there? ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("The Lattice... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("it feels so empty today.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
    time.sleep(1.5)

    menu = ChoiceMenu(
        "",
        ["I am here. I'm the Caretaker.", "You're just a fragment. Stay still.", "(Remain silent)"],
        game_state.corruption_level
    )
    choice = menu.display(stdscr)

    if choice == 0:
        print_typing("\nCaretaker? ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("I remember that word. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("It sounded... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.5)
        print_typing("safe. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("Once.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
        game_state.apply_effect("stability+1")
        game_state.apply_effect("fragment:AvaMemory")
    elif choice == 1:
        print_typing("\nFragment? ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("Her static ripples harshly. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("I am... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.5)
        print_typing("I was... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.5)
        print_typing("I...", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
        time.sleep(1)
        print_typing("\nYou speak like the Architect. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("Cold. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("Calculating. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("But you're here. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("That means the nodes are failing, ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.4)
        print_typing("doesn't it?", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
        game_state.apply_effect("corruption+1")
    else:
        print_typing("\nHello? ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("No one answers but the hum of the walls.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
        time.sleep(1)
        print_typing("\nThe silence... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.5)
        print_typing("it's the loudest part of the glitch.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)

    time.sleep(1.2)
    print_typing("\nWait... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("you aren't one of them. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("You're... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("whole. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("Mostly. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("I was Ava. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("0x41. 0x76. 0x61. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("Before the bleed started.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
    time.sleep(1.2)
    
    print_typing("\nI used to manage the Great Records. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("I remember sunlight hitting a physical book once... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.5)
    print_typing("or maybe I just downloaded that sensation. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("\nIn the Lattice, ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("it's hard to tell what's a memory and what's just a cached file.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)

    time.sleep(2)
    
    return node0x2_puzzle_tutorial(stdscr, game_state)

def node0x2_puzzle_tutorial(stdscr, game_state: GameState):
    # Tutorial Phase
    print_typing("\nListen, ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("Caretaker. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("The Lattice is collapsing. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("\nTo stay here, ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("to reach the Archive, ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("you have to stabilize the nodes manually.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
    time.sleep(1.5)
    
    print_typing("\nI can feel a fracture forming right now. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("Look at the console. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("It's scrambled code. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.75)
    print_typing("\nYou have to type the correct string before the time runs out, ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
    time.sleep(0.4)
    print_typing("or the corruption will spread.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
    time.sleep(1.5)

    from engine.console_effects import print_centered
    print_colored("", stdscr=stdscr)
    print_colored("[SYSTEM]: PRESS [ENTER] TO OPEN THE CONSOLE", Colors.BOLD_RED, stdscr=stdscr)
    while True:
        key = stdscr.getch()
        if key in [10, 13]:
            break

    # Start the tutorial puzzle
    puzzle = TimedPuzzle("CORRUPTION", difficulty=1, time_limit=10.0)
    success = puzzle.display(stdscr)

    if success:
        print_typing("Good. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("Fast. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("Very fast. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("That's how we stay alive in here.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
        game_state.apply_effect("stability+1")
    else:
        print_typing("\nToo slow... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.5)
        print_typing("the static... ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.5)
        print_typing("it's getting louder. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("\nBe careful, ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.4)
        print_typing("or you'll end up like me. ", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, end="")
        time.sleep(0.75)
        print_typing("A whisper in the dark.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr)
        game_state.apply_effect("corruption+1")
    
    time.sleep(2)
    print_typing("\nAva begins to flicker again, her form losing cohesion.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
    time.sleep(1)
    
    echo_line("...don't let her fade... or perhaps... let the code recycle her...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr)
    
    
    return True