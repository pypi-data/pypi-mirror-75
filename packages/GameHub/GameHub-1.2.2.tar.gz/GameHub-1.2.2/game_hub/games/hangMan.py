"""
this is the hangman game
"""
import random

from PyInquirer import prompt
from examples import custom_style_1

from game_hub.utils.file.path import find_file
from game_hub.utils.logging import MyLogger
from game_hub.questions import hangman_questions

logger = MyLogger.logging.getLogger('gamehub.games.hangMan')


def randomise(file_path=None) -> str:
    """
    returns a random word from the hangManWords.txt file
    :return: random word
    """
    if file_path is None:
        file_name = 'hangManWords.txt'
        file_path = find_file(file_name)
        if file_path is None:
            file_path = find_file(file_name, '../')
    with open(file_path, 'r') as hang_man_words:
        hang_man_words_string = hang_man_words.read()
    words = hang_man_words_string.split()
    random_word_picker = random.randint(0, len(words) - 1)
    return words[random_word_picker]


def hiding(word: str) -> str:
    """
    takes a word and replaces all characters with underscores
    :return: word with characters as underscores
    """
    hidden_word = ""
    counter = 0
    broken_up_random_word = list(word)
    number_of_letters_in_random_word: int = len(broken_up_random_word)
    while counter != number_of_letters_in_random_word:
        hidden_word += "_"
        counter += 1
    the_word = ' '.join(list(hidden_word))
    logger.info(the_word)
    return hidden_word


def hang_man_game(word: str, hidden_word: str, debug: str = None) -> str:
    """
    it loops while the player hasn't won or lost yet, and when it loops it asked the user for a letter, an if it's
    in the word then it replaces the space where the letter was originally in the hidden word and then prints it, if
    they get it wrong then the function takes off one life and prints incorrect then the hidden word again. if the
    user types in the full word or they guess letter by letter they win, but lose if they run out of lives
    :param debug: string to confirm if you are debugging, and if you are, then is it a test or manual debugging
    :param word: the word that the user has to guess
    :param hidden_word: the word but all chars are replaced with underscores
    """
    guess = ''
    debug_word_picker = 0
    hidden_word_chars = list(hidden_word)
    chances: int = 10
    word_chars = list(word)
    while word_chars != hidden_word_chars and chances > 0:
        if debug is not None:
            if debug == "test":
                guess = debug[debug_word_picker]
            elif debug == "manual":
                guess = input("enter 'guess': ")
        else:
            guess = prompt(hangman_questions[0], style=custom_style_1).get("hangman_guess")
        if guess == word:
            break
        hidden_word_chars, is_guess_correct = replace_space_with_guess(guess, word_chars, hidden_word_chars)
        logger.info(" ".join(hidden_word_chars))
        if not is_guess_correct:
            chances -= 1
            logger.info("incorrect!")
            if chances > 1:
                logger.info("You have " + str(chances) + " lives left")
            elif chances == 1:
                logger.info("You have " + str(chances) + " life left")
        debug_word_picker += 1
    if chances == 0:
        return f"You failed,\nThe word was {word}"
    else:
        return "Congrats, you won!"


def replace_space_with_guess(guess: str, list_word: list, list_hidden_word: list) -> list and bool:
    """
    replaces underscore with guess if the guess is correct
    :return: None
    """
    was_the_guess_correct = False
    for i in range(len(list_word)):
        if guess == list_word[i]:
            was_the_guess_correct = True
            list_hidden_word[i] = guess
    return list_hidden_word, was_the_guess_correct


def game() -> None:
    """
    plays the hangman game
    :return:
    """
    logger.info("the hang man game has been picked")
    random_word = randomise()
    end_message = hang_man_game(random_word, hiding(random_word))
    logger.info(end_message)


if __name__ == '__main__':
    game()
