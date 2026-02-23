import time
import random
from engine.state_manager import GameState
from engine.console_effects import Colors, print_typing, print_colored, clear_terminal, echo_line
from engine.elements import ChoiceMenu
from engine.save_manager import SaveManager
from engine.audio import AudioManager
from .base_scene import BaseScene

audio = AudioManager()

class Scene1Corridor(BaseScene):
    def run(self, stdscr, game_state: GameState) -> str:
        player_name = game_state.player_name
        # Save point at start of scene
        SaveManager.save_game(game_state, "scene1_identity_sequence")
        
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
        print_typing(" Something presses against the walls of code.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
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
            self.explore(stdscr, game_state)
        elif choice == 1:
            self.stand_still(stdscr, game_state)

        menu = ChoiceMenu(None, ["Follow the guiding whispers", "Defy the pull and resist"], game_state.corruption_level)
        choice = menu.display(stdscr)

        if choice == 0:  # follow
            echo_line("...yes... deeper... don’t turn back now...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
            game_state.apply_effect("corruption+2")
            return self.part2(stdscr, game_state, path="follow")
        elif choice == 1:  # resist
            echo_line("...no... don’t leave me here...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
            game_state.apply_effect("stability+2")
            return self.part2(stdscr, game_state, path="resist")
            
        return "node0x2_ava_intro"

    def explore(self, stdscr, game_state: GameState):
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

        echo_line("You… are not alone…", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr, end="\n\n")
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
        game_state.apply_effect("stability-1")
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

    def stand_still(self, stdscr, game_state: GameState):
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
        game_state.apply_effect("fragment:shard_001")
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

    def part2(self, stdscr, game_state: GameState, path: str) -> str:
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
        
        print_colored("<<< EXITING NODE 0x1 >>>\n", Colors.BOLD_BLACK, stdscr=stdscr)
        time.sleep(1)
        
        from dialogue import intro_systems_rebooting_bar
        intro_systems_rebooting_bar(stdscr, duration=3.0, color=Colors.BOLD_CYAN)
        clear_terminal(stdscr)
        
        return "node0x2_ava_intro"
