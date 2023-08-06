"""
contains all the questions that need to be asked by the games
"""
from prompt_toolkit.validation import Validator, ValidationError
import regex
import csv

from pathlib import Path


def read_picked_slots() -> list:
    """
    This reads the picked_slots.csv and gets a list of picked slots

    :return: a list of picked slots
    """
    with open(Path.home() / '.gamehub/picked_slots.csv', newline='') as picked_slots_csv:
        picked_slots_rows = csv.reader(picked_slots_csv, delimiter=' ', quotechar='|')
        picked_slots = []
        for row in picked_slots_rows:
            picked_slots.append(row[0])
    return picked_slots


class IntValidator(Validator):
    """
    thing
    """

    def validate(self, document) -> None:
        """
        validates the input
        """

        not_ok = regex.search('[^0-9]', document.text)
        if not_ok:
            raise ValidationError(
                message='Please enter a int',
                cursor_position=len(document.text)
            )


class OneToNineValidator(Validator):
    """
    thing
    """

    def validate(self, document) -> None:
        """
        validates the input
        """
        has_already_been_picked = False
        picked_slots = read_picked_slots()
        for i in range(picked_slots.__len__()):
            if str(picked_slots[i]) in document.text:
                has_already_been_picked = True
        is_not_from_1_to_9 = not regex.match('^[0-9]{1}$', document.text)
        if is_not_from_1_to_9 or has_already_been_picked:
            raise ValidationError(
                message="Please enter a int from one to nine that hasn't been picked yet",
                cursor_position=len(document.text)
            )


class StringValidator(Validator):
    """
    thing
    """

    def validate(self, document) -> None:
        """
        validates the input
        """

        ok = regex.match('^[a-zA-Z]{1,11}$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a string that is less than 10 characters',
                cursor_position=len(document.text)
            )


tic_questions = [
    # question 1 - Tutorial
    {
        'type': 'confirm',
        'message': 'Do you want to see the tutorial?',
        'name': 'tutorial',
        'default': True
    },
    # question 2 - Difficulty level
    {
        'type': 'list',
        'name': 'difficulty',
        'message': 'What difficulty level do you want?',
        'choices': ['Easy', 'Medium', 'Hard', 'Custom'],
    },
    # question 3 - freq of lose
    {
        'type': 'input',
        'name': 'freq_lose',
        'message': 'frequency of losing moves:',
        'validate': IntValidator
    },
    # question 4 - freq of draw
    {
        'type': 'input',
        'name': 'freq_draw',
        'message': 'frequency of drawing moves:',
        'validate': IntValidator
    },
    # question 5 - freq of win
    {
        'type': 'input',
        'name': 'freq_win',
        'message': 'frequency of winning moves:',
        'validate': IntValidator
    },
    # question 6 - confirm frequencies
    {
        'type': 'confirm',
        'name': 'confirm_choices',
        'message': 'Are you sure about these choices?',
    },
    # question 7 - human or ai
    {
        'type': 'confirm',
        'name': 'human_or_ai',
        'message': 'Do you want to play against the AI?',
    },
    # question 8 - pick a slot
    {
        'type': 'input',
        'name': 'picked_slot',
        'message': 'Pick a slot:',
        'validate': OneToNineValidator
    },
]

hangman_questions = [
    {
        'type': 'input',
        'message': 'Type your guess:',
        'name': 'hangman_guess',
        'validate': StringValidator
    },
]

rps_questions = [
    {
        'type': 'list',
        'name': 'rps',
        'message': 'Pick rock paper or scissors: ',
        'choices': ['Rock', 'Paper', 'Scissors'],
    },
]
