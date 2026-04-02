def display_success_message(stdscr, getch_func=None):
    for message in INITIATION_SUCCESS_MESSAGES:
        audio.play_sound("beep.mp3")
        print_colored(message, Colors.GREEN, stdscr=stdscr)
        time.sleep(1)
