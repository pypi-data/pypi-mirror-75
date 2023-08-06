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


def hang_man_game(word: str, hidden_word: str) -> str:
    """
    it loops while the player hasn't won or lost yet, and when it loops it asked the user for a letter, an if it's
    in the word then it replaces the space where the letter was originally in the hidden word and then prints it, if
    they get it wrong then the function takes off one life and prints incorrect then the hidden word again. if the
    user types in the full word or they guess letter by letter they win, but lose if they run out of lives
    :param hidden_word: the word but all letters are replaced with underscores
    :param word: the word that has been picked
    """
    list_hidden_word = list(hidden_word)
    chances: int = 10
    listed_word = list(word)
    while word != hidden_word and chances > 0:
        guess = prompt(hangman_questions[0], style=custom_style_1).get("hangman_guess")
        if guess == word:
            break
        list_hidden_word, is_guess_correct = replace_space_with_guess(guess, listed_word, list_hidden_word)
        logger.info(" ".join(list_hidden_word))
        if not is_guess_correct:
            chances -= 1
            logger.info("incorrect!")
            if chances > 1:
                logger.info("You have " + str(chances) + " lives left")
            elif chances == 1:
                logger.info("You have " + str(chances) + " life left")
    if chances == 0:
        return "You failed,The word was %s" % word
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
    if end_message[0] == "Y":
        logger.info(end_message.split(',')[0])
        logger.info(end_message.split(',')[1])
    else:
        logger.info(end_message)


if __name__ == '__main__':
    game()
