"""
Games cli
"""
import click
from pathlib import Path
import json

from game_hub.games import hangMan, ticTacToe, rockPaperScissors


def change_last_game(game: str) -> None:
    """
    changes the last game to the game just played
    :param game: the new last played game
    :return: nothing
    """
    last_game_path = Path.home() / '.gameHub/lastGame.json'
    try:
        json_file = json.loads(last_game_path.read_text())
        json_file['last_game'] = game
        with last_game_path.open(mode='w') as json_output:
            json.dump(json_file, json_output, indent=4)
    except FileNotFoundError:
        # creates file
        json_file = open(str(last_game_path), 'w')
        json.dump({'last_game': game}, json_file, indent=4)
        json_file.close()


@click.group('play', short_help='group of all games')
def play() -> None:
    """Contains all games"""
    pass


@play.command('hang', short_help='Plays Hangman game')
def hangman() -> None:
    """Plays Hangman game"""
    hangMan.game()
    change_last_game('hangman')


@play.command('rps', short_help='Plays Rock Paper Scissors game')
def rps() -> None:
    """Plays rock paper scissors game"""
    rockPaperScissors.game()
    change_last_game('rps')


@play.command('tic', short_help='Plays Tic Tac Toe game')
def tictactoe() -> None:
    """Plays Tic tac toe game"""
    ticTacToe.game()
    change_last_game('tictactoe')
