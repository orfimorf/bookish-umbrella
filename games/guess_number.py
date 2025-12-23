import random
from games.base import BaseGame

class GuessNumberGame(BaseGame):
    name = "guess_number"

    def __init__(self):
        self.secret = random.randint(1, 100)
        self.attempts = 0

    def start(self) -> str:
        return "🎮 Я загадал число от 1 до 100. Попробуй угадать!"

    def handle_input(self, user_input: str) -> tuple[str, bool]:
        try:
            guess = int(user_input.strip())
        except ValueError:
            return "🔢 Пожалуйста, пришлите целое число от 1 до 100.", False

        if guess < 1 or guess > 100:
            return "⚠️ Число должно быть от 1 до 100.", False

        self.attempts += 1

        if guess < self.secret:
            return "⬆️ Больше!", False
        elif guess > self.secret:
            return "⬇️ Меньше!", False
        else:
            return f"🎉 Угадал! Загаданное число: {self.secret}.", True