from abc import ABC, abstractmethod
from typing import Dict, Type



class BaseGame(ABC):
    name: str  # например, "guess_number"

    @abstractmethod
    def start(self) -> str:
        pass

    @abstractmethod
    def handle_input(self, user_input: str) -> tuple[str, bool]:
        pass


GAME_REGISTRY: Dict[str, Type[BaseGame]] = {}

def register_game(game_class: Type[BaseGame]):
    GAME_REGISTRY[game_class.name] = game_class
    return game_class