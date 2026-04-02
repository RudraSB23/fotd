from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
from engine.core.state_manager import GameState

class BaseScene(ABC):
    def __init__(self):
        self.scene_id = self.__class__.__name__.lower()

    @abstractmethod
    def run(self, stdscr, game_state: GameState, getch_func=None) -> str:
        """Returns next scene_id or None to end game"""
        pass
