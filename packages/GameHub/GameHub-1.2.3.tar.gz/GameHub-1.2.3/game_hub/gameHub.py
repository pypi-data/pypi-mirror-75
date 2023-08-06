"""
An interface to play multiple games
"""
import random
import json
from pathlib import Path
from difflib import get_close_matches
from typing import Callable

from game_hub.games import hangMan, ticTacToe, rockPaperScissors
from game_hub.games.gameCLI import change_last_game
from game_hub.utils.logging import MyLogger


logger = MyLogger.logging.getLogger('gamehub.gamehub')
gamehub_directory = Path.home() / '.gameHub'

last_game_played: Callable
last_game: Callable

convert_str_to_game_func = {
    "tictactoe": ticTacToe.game,
    "hangman": hangMan.game,
    "rps": rockPaperScissors.game
}
convert_game_func_to_str = {
    rockPaperScissors.rps_game: "rps",
    ticTacToe.game: "tictactoe",
    hangMan.game: "hangman"
}
cmd_name_to_game_name = {
    "tic": "tictactoe",
    "hang": "hangman",
    "rps": "rps",
}


def generate() -> Callable:
    """
    Pick Random Game to play
    :return: picked game
    """
    list_games = [rockPaperScissors.rps_game, hangMan.game, ticTacToe.game]
    picked_game = list_games[random.randint(0, 2)]
    change_last_game(convert_game_func_to_str[picked_game])
    return picked_game


def play_random_game_from_list(games: iter) -> Callable or str:
    """
    play's a random game from a given list. if one of the games is spelt wrong it prints the closest matching command
    in case they misspell them.
    :param games: list of games to randomly chose from
    """
    for game in games:
        if game not in cmd_name_to_game_name.keys():
            closest_matching_command = get_close_matches(game, cmd_name_to_game_name.keys())
            fail_message = f"{game} is not an available game"
            if closest_matching_command:
                fail_message += f"\nDid you mean: {closest_matching_command[0]}?"
            else:
                fail_message += "\nSee all games by entering gamehub play or just play if you are in a repl"
            return fail_message
    for i in range(len(games)):
        games[i] = cmd_name_to_game_name[games[i]]
    return games[random.randint(0, 1)]


def play_again(json_file_path: Path) -> None:
    """
    plays the last game you played
    """
    json_file_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Playing the last game")
    try:
        config = json.loads(json_file_path.read_text())
        logger.info(config['last_game'])
        if not config["last_game"]:
            logger.info("you haven't played a game yet")
        else:
            convert_str_to_game_func[config["last_game"]]()
    except FileNotFoundError:
        logger.warning("you haven't played a game yet")
        with open(str(json_file_path), 'w') as lastGame:
            json.dump({"last_game": None}, lastGame, indent=4)
