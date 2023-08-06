"""
this is the rock paper scissors game
"""
import random

from PyInquirer import prompt
from examples import custom_style_1

from game_hub.utils.logging import MyLogger
from game_hub.questions import rps_questions


logger = MyLogger.logging.getLogger('gamehub.games.hangMan')


def check_who_won(user_choice: str, computer_choice: str) -> str:
    """
    given a user input and computer guess it compares them to see who would have won in a rock paper scissors match,
    note that the user input has to be at minimum transformed into either 'S', 'R' or 'P' for 'Scissors', 'Rock', and
    'paper'
    :param computer_choice: the computer's choice
    :param user_choice: the user's choice
    :return:
    """

    if user_choice == "Rock":
        if computer_choice == "rock":
            return "we drew"
        elif computer_choice == "scissors":
            return "you win"
        else:
            return "you lose"

    if user_choice == "Scissors":
        if computer_choice == "rock":
            return "you lose"
        elif computer_choice == "scissors":
            return "we drew"
        else:
            return "you win"

    if user_choice == "Paper":
        if computer_choice == "rock":
            return "you win"
        elif computer_choice == "scissors":
            return "you lose"
        else:
            return "we drew"


def rps_game() -> str:
    """
    this method asks the user to user to input three strings, rock paper and scissors, and if they input something else
    then they ask again, after it has a good input the method picks one of them randomly and then compares against the
    user to see who won.
    :return: who won
    """
    computer_choice = ["rock", "paper", "scissors"][random.randint(0, 2)]

    logger.info("Type in one of the three choices and I'll print mine.")
    user_choice = prompt(rps_questions[0], style=custom_style_1).get("rps")
    logger.info("the computer picked: " + computer_choice)
    return check_who_won(user_choice, computer_choice)


def game() -> None:
    """
    Plays Rock Paper Scissors
    """
    logger.info("The rock paper scissors game has been picked")
    logger.info(rps_game())


if __name__ == '__main__':
    game()
