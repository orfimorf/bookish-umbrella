# bot/session.py
from typing import Dict, Optional, Type
from games.base import BaseGame
from games.base import GAME_REGISTRY


class UserSession:
    def __init__(self):
        self.current_game: Optional[BaseGame] = None
        self.game_name: Optional[str] = None

    def start_game(self, game_name: str) -> str:
        if game_name not in GAME_REGISTRY:
            return "❌ Игра не найдена."
        self.game_name = game_name
        self.current_game = GAME_REGISTRY[game_name]()
        return self.current_game.start()

    def handle_input(self, user_input: str) -> str:
        if not self.current_game:
            return "Начни игру командой /start."

        message, is_finished = self.current_game.handle_input(user_input)
        if is_finished:
            # Можно сразу начать новую, или оставить выбор — здесь просто завершаем
            self.current_game = None
            return message + "\n\nИгра завершена. Начни новую: /start"
        return message

from games import guess_number