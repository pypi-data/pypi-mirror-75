"""
tests all functions in gameHub.py
"""
# import json

import pytest
# from pathlib import Path

from game_hub import gameHub
from game_hub.games import hangMan, rockPaperScissors, ticTacToe

list_games = [rockPaperScissors.rps_game, hangMan.game, ticTacToe.game]


def test_generate() -> None:
    """
    tests generate() function by making two lists of randomly generated games. Then it tests if the results are games
    and not just any random value. If they aren't games, then it fails. Finally it tests if the randomly generated lists
    aren't the same. If they are the same, then it fails.
    """
    random_results_1 = []
    random_results_2 = []
    for _ in range(9):
        random_results_1.append(gameHub.generate())
        random_results_2.append(gameHub.generate())
    for random_result_1 in random_results_1:
        assert random_result_1 in list_games
    for random_result_2 in random_results_2:
        assert random_result_2 in list_games
    assert random_results_1 != random_results_2


@pytest.mark.parametrize("games,expected",
                         [(['tic', 'rps'], ['tictactoe', 'rps']),
                          (['rps', 'hang'], ['rps', 'hangman']),
                          (['tic', 'hang'], ['tictactoe', 'hangman']),
                          (['ti', 'hang'], "ti is not an available game\nDid you mean: tic?")
                          ])
def test_play_random_game_from_list(games: list, expected: list) -> None:
    """
    tests play_random_game_from_list() function in gameHub.py
    """
    actual_output = gameHub.play_random_game_from_list(list(games))
    random_results_1 = []
    random_results_2 = []
    if not isinstance(expected, str):
        assert actual_output in expected
        for _ in range(20):
            random_results_1.append(gameHub.play_random_game_from_list(list(games)))
            random_results_2.append(gameHub.play_random_game_from_list(list(games)))
        assert random_results_1 != random_results_2
    else:
        assert actual_output == expected


def test_play_again() -> None:
    """
    tests the play_again function in gameHub.py
    :return:
    """
    pass
    # file = './test_data/mock_dir/mock_dir/test_lastGame.json'
    # Path.rmdir(Path('test_data/mock_dir'))
    # gameHub.play_again(Path(file))
    # with open(file, 'r') as json_file:
    #     json_file_content = json.load(json_file)
