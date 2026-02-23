import time
from engine.state_manager import GameState
from engine.console_effects import Colors, print_typing, print_colored, echo_line
from engine.elements import ChoiceMenu, TimedPuzzle
from engine.save_manager import SaveManager
from engine.audio import AudioManager
from .base_scene import BaseScene

audio = AudioManager()

class Scene2Ava(BaseScene):
    def run(self, stdscr, game_state: GameState) -> str:
        SaveManager.save_game(game_state, "node0x2_ava_intro")
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
            game_state.add_fragment("AvaMemory")
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
        
        return self.puzzle_tutorial(stdscr, game_state)

    def puzzle_tutorial(self, stdscr, game_state: GameState) -> str:
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

        print_colored("", stdscr=stdscr)
        print_colored("[SYSTEM]: PRESS [ENTER] TO OPEN THE CONSOLE", Colors.BOLD_RED, stdscr=stdscr)
        while True:
            key = stdscr.getch()
            if key in [10, 13]:
                break

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
            game_state.puzzles_solved += 1
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
            game_state.puzzles_failed += 1
        
        time.sleep(2)
        print_typing("\nAva begins to flicker again, her form losing cohesion.", 0.04, Colors.BOLD_BLACK, stdscr=stdscr)
        time.sleep(1)
        
        echo_line("...don't let her fade... or perhaps... let the code recycle her...", 0.04, Colors.BOLD_MAGENTA, stdscr=stdscr)
        
        return None # End of current content
