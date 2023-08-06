"""
this is the tic tac toe game
"""
import random
import csv

from pathlib import Path
from PyInquirer import prompt
from examples import custom_style_1
from clint.textui import colored

from game_hub.utils.logging import MyLogger
from game_hub.questions import tic_questions

logger = MyLogger.logging.getLogger('gamehub.games.ticTacToe')
picked_slots_path = Path.home() / '.gamehub/picked_slots.csv'

evaluation_to_message = {
    "player 1": "player 1 won",
    "player 2": "player 2 won",
    "ai": "ai won",
    "tie": "It is a draw",
    "human": "you won"
}
potential_scores = {
    "player 1": 1,
    "tie": 0,
    "player 2": -1
}
switch_player = {
    "player 1": "player 2",
    "player 2": "player 1"
}
board_keys = [
    "top_left", "top_mid", "top_right",
    "mid_left", "mid_mid", "mid_right",
    "bot_left", "bot_mid", "bot_right"
]


def pick_ai_move(board: dict, current_player: str, ai_difficulty_lvl: str) -> int:
    """
    using the mini_max function, it loops through all the moves for this turn and then finds out the best one by calling
    mini_max, and dependant on who's turn it is, the computer either saves the best score by looking for the lowest
    score (meaning player two's best move) or the highest score (meaning player one's best move)
    :param ai_difficulty_lvl: The difficulty level of the ai
    :param board: the tic tac toe board
    :param current_player: player who has the turn
    """
    if current_player == "player 1":
        maximising_player = False
        symbol_to_put_in_slot = "x"
    else:
        maximising_player = True
        symbol_to_put_in_slot = "o"
    best_move = float("-inf")
    mini_best_score = float("-inf")
    max_best_score = float("inf")
    if all(x == "-" for x in board.values()):
        return random.randint(0, 8)
    while best_move == float("-inf"):
        for i in range(9):
            if board[board_keys[i]] == '-':
                board[board_keys[i]] = symbol_to_put_in_slot
                score = mini_max(board, maximising_player)
                if ai_difficulty_lvl == "win":
                    if score > mini_best_score and not maximising_player:
                        mini_best_score = score
                        best_move = i
                    if score < max_best_score and maximising_player:
                        max_best_score = score
                        best_move = i
                if ai_difficulty_lvl == "draw":
                    if score == 0 and not maximising_player:
                        mini_best_score = score
                        best_move = i
                    if score == 0 and maximising_player:
                        max_best_score = score
                        best_move = i
                if ai_difficulty_lvl == "lose":
                    if score == -1 and not maximising_player:
                        mini_best_score = score
                        best_move = i
                    if score == 1 and maximising_player:
                        mini_best_score = score
                        best_move = i
                board[board_keys[i]] = "-"
        if ai_difficulty_lvl == "draw":
            ai_difficulty_lvl = "win"
        if ai_difficulty_lvl == "lose":
            ai_difficulty_lvl = "draw"
    return best_move


def evaluate_board(board: dict, ai_player: str = None) -> str:
    """
    takes in a board as a dictionary and a list and then uses them to check who is the winner, loser or if it is a tie
    or the game hasn't finished yet.
    :param ai_player: if the user is playing against the ai, which player is the ai
    :param board: dictionary of all slots on the game board
    :return: the winning player, a tie or an empty string if the game is not finished
    """
    winner = ""
    list_board = list(board.values())

    for symbol in ["x", "o"]:
        row_1 = list_board[0] == list_board[1] == list_board[2] == symbol
        row_2 = list_board[3] == list_board[4] == list_board[5] == symbol
        row_3 = list_board[6] == list_board[7] == list_board[8] == symbol

        col_1 = list_board[0] == list_board[3] == list_board[6] == symbol
        col_2 = list_board[1] == list_board[4] == list_board[7] == symbol
        col_3 = list_board[2] == list_board[5] == list_board[8] == symbol

        dia_1 = list_board[0] == list_board[4] == list_board[8] == symbol
        dia_2 = list_board[2] == list_board[4] == list_board[6] == symbol
        if row_1 or row_2 or row_3 or col_1 or col_2 or col_3 or dia_1 or dia_2:
            winner = {'x': 'player 1', 'o': 'player 2', }[symbol]
            break
    if winner == "":
        for value in board.values():
            if value == "-":
                return ""
        return "tie"
    if ai_player:
        human_player = switch_player[ai_player]
        if ai_player == winner:
            winner = "ai"
        if human_player == winner:
            winner = "human"
    return winner


def mini_max(board: dict, maximizing_player: bool) -> int:
    """
    Scoring system: 1 -> win | 0 -> draw | -1 -> lose

    Given a board and the maximising player, it loops through the board, checks for an empty space, and if there is
    then it puts x into it and then calls itself, but switches the maximising player, so it then puts an o into the
    space, this keeps on going till the board is completed and it does an evaluation of the score, this is then
    compared to the worst score for that player (X's would be -infinity, and vice versa) as the variable best_score
    and if the new evaluation is better than best_score, it is assigned to best_score. it goes on to the next
    possible ending and then compares that to the current score and if it's better replaces it. this keeps on going
    till all endings are done and the best ending is saved, then you go one up and then check the next branch in the
    tree. It then checks all these branches, gets the best branch and goes up again, and repeats until it get's back
    to the top.

    :param board: the game board
    :param maximizing_player: the current player
    :return: what will happen if the ai goes here
    """

    if evaluate_board(board) != "":
        return potential_scores[evaluate_board(board)]

    if maximizing_player:
        max_best_move = float('-inf')
        for i in range(9):
            if board[board_keys[i]] == '-':
                board[board_keys[i]] = "x"
                score = mini_max(board, False)
                board[board_keys[i]] = "-"
                if score > max_best_move:
                    max_best_move = score
        return max_best_move
    else:
        min_best_move = float('inf')
        for i in range(9):
            if board[board_keys[i]] == '-':
                board[board_keys[i]] = "o"
                score = mini_max(board, True)
                board[board_keys[i]] = "-"
                if score < min_best_move:
                    min_best_move = score
        return min_best_move


def choose_difficulty() -> list:
    """
    picks the ai difficulty or gives the option for the user to create their own difficulty
    :return: a list which decides the difficulty of the ai with three possible variables
    """
    user_difficulty_lvl = prompt(tic_questions[1], style=custom_style_1).get("difficulty")

    freq_lose = 2
    freq_draw = 6
    freq_win = 6
    if user_difficulty_lvl == "Hard":
        freq_lose = 1
        freq_draw = 0
        freq_win = 16
    elif user_difficulty_lvl == "Easy":
        freq_lose = 10
        freq_draw = 2
        freq_win = 2
    elif user_difficulty_lvl == "Custom":
        confirm_choices = False
        while not confirm_choices:
            freq_lose = int(prompt(tic_questions[2], style=custom_style_1).get("freq_lose"))
            freq_draw = int(prompt(tic_questions[3], style=custom_style_1).get("freq_draw"))
            freq_win = int(prompt(tic_questions[4], style=custom_style_1).get("freq_win"))
            confirm_choices = prompt(tic_questions[5], style=custom_style_1).get("confirm_choices")
    return list((["lose"] * freq_lose) + (["draw"] * freq_draw) + (["win"] * freq_win))


def print_board(board: dict):
    """
    saves the three rows of the tic, tac toe board and into separate variables and then prints them with a space between
    each board
    :return: nothing
    """
    i = 0
    for key, value in board.items():
        i += 1
        if value == "-":
            board[key] = i
        if value == "x":
            board[key] = (getattr(colored, 'red')('X'))
        if value == "o":
            board[key] = (getattr(colored, 'blue')('O'))

    return (f"""
    {board['top_left']}  {board['top_mid']}  {board['top_right']}
    {board['mid_left']}  {board['mid_mid']}  {board['mid_right']}
    {board['bot_left']}  {board['bot_mid']}  {board['bot_right']}
    """)


def tutorial() -> None:
    """
    Asks if they want to see the tutorial, and if they do prints a string explaining the game
    """
    user_wants_tutorial = prompt(tic_questions[0], style=custom_style_1).get("tutorial")
    if user_wants_tutorial:
        logger.info("""
    You pick the slot you want to pick using a number e.g

    -  -  -
    -  -  -
    -  -  -

    Is this:

    1  2  3
    4  5  6
    7  8  9

    To win get three in a row

    Here we'll show an example game so you don't screw up

    Player one it's your turn!

    Player one: 3

    -  -  x
    -  -  -
    -  -  -

    Player 2 it's your turn!

    Player 2: 6

    -  -  x
    -  -  o
    -  -  -

    ...And so on until one of the players get's three in a row

        """)


def append_to_picked_slots(picked_slot: int) -> None:
    """
    saves all the picked slots to a file to be used by questions
    """
    with open(picked_slots_path, 'a', newline='') as picked_slots:
        spam_writer = csv.writer(picked_slots, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spam_writer.writerow([picked_slot])


class TicTacToe:
    """
    holds the game code
    """

    def __init__(self) -> None:
        self.board = {
            "top_left": "-", "top_mid": "-", "top_right": "-",
            "mid_left": "-", "mid_mid": "-", "mid_right": "-",
            "bot_left": "-", "bot_mid": "-", "bot_right": "-"
        }
        self.top_row = f"{self.board['top_left']}  {self.board['top_mid']}  {self.board['top_right']}"
        self.mid_row = f"{self.board['mid_left']}  {self.board['mid_mid']}  {self.board['mid_right']}"
        self.bot_row = f"{self.board['bot_left']}  {self.board['bot_mid']}  {self.board['bot_right']}"
        self.end_state_of_game = ""
        self.list_picked_slots = []
        self.ai_difficulty_lvls = []

    def tictactoe_game(self) -> str:
        """
        checks if any one has one yet and if they have then return who is the winner, if no one has won then
        it picks the player who is going first, prints the board, asks the user to pick a slot and replaces the slot
        with the user's mark (x or o). After that, it checks if there is a tie (if so it breaks the loop) and if there
        isn't then it continues until the match has finished. Finally after the loop breaks it checks who won and then
        prints the winner.
        """
        logger.info("the tic tac toe game has been picked")
        list_of_players = ["player 1", "player 2"]
        tutorial()
        ai_player = ""
        user_has_picked_ai = prompt(tic_questions[6], style=custom_style_1).get("human_or_ai")
        current_player = random.choice(list_of_players)

        picked_slots_path.parent.mkdir(parents=True, exist_ok=True)
        open(picked_slots_path, 'w').close()
        if user_has_picked_ai:
            ai_player = random.choice(list_of_players)
            self.ai_difficulty_lvls = choose_difficulty()

        while self.end_state_of_game == '':
            current_player = switch_player[current_player]
            print(print_board(dict(self.board)))
            if user_has_picked_ai and ai_player == current_player:
                logger.info("it is the AI's turn")
            elif not user_has_picked_ai:
                logger.info("it is " + current_player + "'s turn")
            else:
                logger.info("it is your turn")
            if user_has_picked_ai and current_player == ai_player:
                ai_difficulty_lvl = self.ai_difficulty_lvls[random.randint(0, len(self.ai_difficulty_lvls) - 1)]
                picked_slot = pick_ai_move(self.board, current_player, ai_difficulty_lvl) + 1
            else:
                picked_slot = int(prompt(tic_questions[7], style=custom_style_1).get("picked_slot"))
            self.list_picked_slots.append(picked_slot)
            append_to_picked_slots(picked_slot)
            player_symbol = {'player 1': 'x', 'player 2': 'o', }[current_player]
            self.board[board_keys[picked_slot - 1]] = player_symbol
            self.end_state_of_game = evaluate_board(self.board, ai_player=ai_player)

        print(print_board(dict(self.board)))
        return evaluation_to_message[self.end_state_of_game]


def game() -> None:
    """
    thing
    """
    tic_tac_toe = TicTacToe()
    logger.info(tic_tac_toe.tictactoe_game())


if __name__ == '__main__':
    game()
