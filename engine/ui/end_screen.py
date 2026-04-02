from engine.ui.console_effects import Colors
from engine.ui.elements import MessageBox
from engine.core.state_manager import GameState

class EndScreen:
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def display(self, stdscr):
        stats = [
            ("SESSION TERMINATED", Colors.BOLD_MAGENTA),
            "",
            f"Subject: {self.game_state.player_name}",
            f"Final Stability: {self.game_state.stability}",
            f"Final Corruption: {self.game_state.corruption_level}",
            f"Fragments Collected: {len(self.game_state.identity_fragments)}",
            f"Puzzles Solved: {self.game_state.puzzles_solved}",
            f"Total Playtime: {self.game_state.playtime_seconds:.0f}s",
        ]

        box = MessageBox(stats, title="TO BE CONTINUED", border_color=Colors.BOLD_MAGENTA)
        box.display(stdscr)
