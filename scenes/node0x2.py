import curses
import time

from engine.core.audio import AudioManager
from engine.core.save_manager import SaveManager
from engine.core.state_manager import GameState
from engine.ui.console_effects import (
    Colors,
    clear_terminal,
    echo_line,
    full_screen_glitch,
    print_centered,
    print_colored,
    print_glitch,
    print_typing,
)
from engine.ui.elements import ChoiceMenu, TimedPuzzle

from .base_scene import BaseScene

audio = AudioManager()


class Scene2Ava(BaseScene):
    def run(self, stdscr, game_state: GameState, getch_func=None) -> str:
        SaveManager.save_game(game_state, "node0x2_ava_intro")

        clear_terminal(stdscr)
        audio.play_sound("beep.mp3")

        for i in range(20):
            print_glitch(
                "<<< ENTERING NODE 0x2: FRAGMENT ALPHA >>>",
                base_color=Colors.BOLD_GREEN,
                glitch_color=True,
                stdscr=stdscr,
                getch_func=getch_func,
                center=True,
                intensity=1 - (i * 0.05),
            )
            time.sleep(0.05)
        clear_terminal(stdscr)
        print_centered(
            "<<< ENTERING NODE 0x2: FRAGMENT ALPHA >>>",
            color=Colors.BOLD_GREEN,
            stdscr=stdscr,
            offset=-1,
        )
        time.sleep(1.0)
        clear_terminal(stdscr)
        time.sleep(1.0)

        print_typing(
            "The scenery shifts. ",
            0.04,
            Colors.BOLD_BLACK,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.4)
        print_typing(
            "The endless corridor collapses into a single, small room.",
            0.04,
            Colors.BOLD_BLACK,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(0.8)
        print_typing(
            "There is a flicker in the center, a figure made of data shards.",
            0.04,
            Colors.BOLD_BLACK,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(1.2)

        echo_line(
            "\n...Ava?...\n",
            0.06,
            Colors.BOLD_MAGENTA,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(0.5)

        print_typing(
            "\nThe figure stabilizes for a moment. ",
            0.04,
            Colors.BOLD_BLACK,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        print_typing(
            "She looks at you with eyes that aren't quite aligned.",
            0.04,
            Colors.BOLD_BLACK,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(1)

        print_typing(
            "\nIs... ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.5)
        print_typing(
            "is someone there? ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "The Lattice... ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.5)
        print_typing(
            "it feels so empty today.",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(1.5)

        menu = ChoiceMenu(
            "",
            [
                "I am here. I'm the Caretaker.",
                "You're just a fragment. Stay still.",
                "(Remain silent)",
            ],
            game_state.corruption_level,
        )
        choice = menu.display(stdscr, getch_func=getch_func)

        if choice == 0:
            print_typing(
                "\nCaretaker? ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "I remember that word. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "It sounded... ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.5)
            print_typing(
                "safe. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "Once.", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, getch_func=getch_func
            )
            game_state.apply_effect("stability+1")
            game_state.add_fragment("AvaMemory")
        elif choice == 1:
            print_typing(
                "\nFragment? ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "Her static ripples harshly. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "I am... ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.5)
            print_typing(
                "I was... ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.5)
            print_typing(
                "I...", 0.04, Colors.BOLD_CYAN, stdscr=stdscr, getch_func=getch_func
            )
            time.sleep(1)
            print_typing(
                "\nYou speak like the Architect. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "Cold. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "Calculating. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "But you're here. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "That means the nodes are failing, ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.4)
            print_typing(
                "doesn't it?",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                getch_func=getch_func,
            )
            game_state.apply_effect("corruption+1")
        else:
            print_typing(
                "\nHello? ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "No one answers but the hum of the walls.",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                getch_func=getch_func,
            )
            time.sleep(1)
            print_typing(
                "\nThe silence... ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.5)
            print_typing(
                "it's the loudest part of the glitch.",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                getch_func=getch_func,
            )

        time.sleep(1.2)
        print_typing(
            "\nWait... ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.5)
        print_typing(
            "you aren't one of them. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "You're... ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.5)
        print_typing(
            "whole. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "Mostly. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "I was Ava. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "0x41 0x76 0x61. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "Before the bleed started.",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(1.2)

        print_typing(
            "\nI used to manage the Great Records. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "I remember sunlight hitting a physical book once... ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.5)
        print_typing(
            "or maybe I just downloaded that sensation. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "\nIn the Lattice, ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.4)
        print_typing(
            "it's hard to tell what's a memory and what's just a cached file.",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            getch_func=getch_func,
        )

        time.sleep(2)

        return self.puzzle_tutorial(stdscr, game_state, getch_func=getch_func)

    def puzzle_tutorial(self, stdscr, game_state: GameState, getch_func=None) -> str:
        print_typing(
            "\nListen, ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.4)
        print_typing(
            "Caretaker. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "The Lattice is collapsing. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "\nTo stay here, ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.4)
        print_typing(
            "to reach the Archive, ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.4)
        print_typing(
            "you have to stabilize the nodes manually.",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(1.5)

        print_typing(
            "\nI can feel a fracture forming right now. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "Look at the console. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "It's scrambled code. ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.75)
        print_typing(
            "\nYou have to type the correct string before the time runs out, ",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            end="",
            getch_func=getch_func,
        )
        time.sleep(0.4)
        print_typing(
            "or the corruption will spread.",
            0.04,
            Colors.BOLD_CYAN,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(1.5)

        print_colored("", stdscr=stdscr)
        print_colored(
            "[SYSTEM]: PRESS [ENTER] TO OPEN THE CONSOLE",
            Colors.BOLD_RED,
            stdscr=stdscr,
        )
        while True:
            getch = getch_func or stdscr.getch
            key = getch()
            if key == -999:
                return -999
            if key in [10, 13]:
                break

        puzzle = TimedPuzzle("CORRUPTION", difficulty=1, time_limit=10.0)
        success = puzzle.display(stdscr, getch_func=getch_func)

        if success:
            print_typing(
                "Good. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "Fast. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "Very fast. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "That's how we stay alive in here.",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                getch_func=getch_func,
            )
            game_state.apply_effect("stability+1")
            game_state.puzzles_solved += 1
        else:
            print_typing(
                "\nToo slow... ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.5)
            print_typing(
                "the static... ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.5)
            print_typing(
                "it's getting louder. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "\nBe careful, ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.4)
            print_typing(
                "or you'll end up like me. ",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                end="",
                getch_func=getch_func,
            )
            time.sleep(0.75)
            print_typing(
                "A whisper in the dark.",
                0.04,
                Colors.BOLD_CYAN,
                stdscr=stdscr,
                getch_func=getch_func,
            )
            game_state.apply_effect("corruption+1")
            game_state.puzzles_failed += 1

        time.sleep(2)
        print_typing(
            "\nAva begins to flicker again, her form losing cohesion.",
            0.04,
            Colors.BOLD_BLACK,
            stdscr=stdscr,
            getch_func=getch_func,
        )
        time.sleep(1)

        echo_line(
            "\n...don't let her fade... or perhaps... let the code recycle her...\n",
            0.04,
            Colors.BOLD_MAGENTA,
            stdscr=stdscr,
            getch_func=getch_func,
        )

        time.sleep(2)

        clear_terminal(stdscr)

        print_colored("<<< EXITING NODE 0x2 >>>\n", Colors.BOLD_BLACK, stdscr=stdscr)
        time.sleep(1)

        return "node0x3_archive"
