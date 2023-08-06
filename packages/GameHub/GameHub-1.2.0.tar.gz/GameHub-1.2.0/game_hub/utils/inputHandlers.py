"""
functions that handle bad inputs in specific circumstances
"""
import re
from game_hub.utils.logging import MyLogger


logger = MyLogger.logging.getLogger('gamehub.utils.inputHandlers')


def check_for_bad_input_strings(user_input: str) -> bool:
    """
    checks if the string is empty, and then if it isn't then checks if it's an int, and finally if it's not an int then
    it returns true
    :param user_input:
    :return:
    """
    if user_input:
        if re.search("[^0-9]", user_input):
            if re.search("[a-zA-Z]", user_input):
                return False
            else:
                logger.info("you put in a symbol, please try again")
        else:
            logger.info("you put in an int, please try again")
    else:
        logger.info("you put in nothing, please try again")
    return True


def check_for_bad_input_int(user_string: str, list_bad_inputs: list, cap: int or float) -> bool:
    """
    given a string, a list of exceptions and a cap, this function checks if the inputted string is an int, it is not
    in the list of exceptions and it is underneath a certain cap. The instructions to avoid the list of exceptions and
    the cap are in the descriptions of the respective parameters.
    :param cap: if the user wants to have a cap, then they can input an int, however if they don't then they can
    put in float("-inf") or float("inf") to stop them from being compared.
    :param user_string: the input that gets tested if it's bad
    :param list_bad_inputs: this list is to check that the input hasn't already been picked in the game
    :return: a boolean that is True if the the input is an int
    """
    if user_string:
        if re.search("[^a-zA-z]", user_string):
            if re.search("[0-9]", user_string):
                user_string = int(user_string)
                if user_string not in list_bad_inputs:
                    if user_string < cap:
                        return False
                    else:
                        logger.info("your input was higher than ten, please try again")
                else:
                    logger.info("your input has already been picked please try again")
            else:
                logger.info("your input had symbols, please try again")
        else:
            logger.info("Your input was a string, please try again")
    else:
        logger.info("you inputted nothing, please try again")
    return True
