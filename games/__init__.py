from games.base import register_game
from games.guess_number import GuessNumberGame
from games.rpc import RockPaperScissorsGame

register_game(GuessNumberGame)
register_game(RockPaperScissorsGame)
