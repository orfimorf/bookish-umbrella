import random
from games.base import BaseGame, register_game

CHOICES = {
    'камень': 0,
    'ножницы': 1,
    'бумага': 2,
}

CHOICE_NAMES = {0: 'камень', 1: 'ножницы', 2: 'бумага'}

@register_game
class RockPaperScissorsGame(BaseGame):
    name = "rps"

    def start(self) -> str:
        return (
            "✌️ Давай сыграем в «Камень, ножницы, бумага»!\n"
            "Просто пришли одно из слов:\n"
            "• камень\n• ножницы\n• бумага"
        )

    def handle_input(self, user_input: str) -> tuple[str, bool]:
        user_choice = user_input.strip().lower()

        if user_choice not in CHOICES:
            valid = ", ".join(list(CHOICES.keys())[:3])  # только русские
            return f"❓ Я не понял. Напиши одно из: {valid}.", False

        user_val = CHOICES[user_choice]
        bot_val = random.randint(0, 2)
        bot_choice = CHOICE_NAMES[bot_val]

        result_msg = f"Ты: {CHOICE_NAMES[user_val]}\nБот: {bot_choice}\n"

        if user_val == bot_val:
            result_msg += "🤝 Ничья!"
        elif (user_val - bot_val) % 3 == 1:
            result_msg += "💀 Ты проиграл!"
        else:
            result_msg += "🎉 Ты победил!"

        # Игра однораундовая — завершаем после хода
        return result_msg + "\n\nСыграем ещё? Просто пришли свой ход!", True