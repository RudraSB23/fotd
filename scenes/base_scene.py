from abc import ABC, abstractmethod
from engine.state_manager import GameState

class BaseScene(ABC):
    def __init__(self):
        self.scene_id = self.__class__.__name__.lower()

    @abstractmethod
    def run(self, stdscr, game_state: GameState) -> str:
        """Returns next scene_id or None to end game"""
        pass
