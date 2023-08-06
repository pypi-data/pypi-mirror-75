"""
contains all the questions that need to be asked by the games
"""
from prompt_toolkit.validation import Validator, ValidationError
import regex


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

        ok = regex.match('^[0-9]{1}$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a int from one to nine',
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
                message='Please enter a int from one to nine',
                cursor_position=len(document.text)
            )


tic_questions = [
    # question 1
    {
        'type': 'confirm',
        'message': 'Do you want to see the tutorial?',
        'name': 'tutorial',
        'default': True
    },
    # question 2
    {
        'type': 'list',
        'name': 'difficulty',
        'message': 'What difficulty level do you want?',
        'choices': ['Easy', 'Medium', 'Hard', 'Custom'],
    },
    # question 3
    {
        'type': 'input',
        'name': 'freq_lose',
        'message': 'frequency of losing moves:',
        'validate': IntValidator
    },
    # question 4
    {
        'type': 'input',
        'name': 'freq_draw',
        'message': 'frequency of drawing moves:',
        'validate': IntValidator
    },
    # question 5
    {
        'type': 'input',
        'name': 'freq_win',
        'message': 'frequency of winning moves:',
        'validate': IntValidator
    },
    # question 6
    {
        'type': 'confirm',
        'name': 'confirm_choices',
        'message': 'Are you sure about these choices?',
    },
    # question 7
    {
        'type': 'confirm',
        'name': 'human_or_ai',
        'message': 'Do you want to play against the AI?',
    },
    # question 8
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
