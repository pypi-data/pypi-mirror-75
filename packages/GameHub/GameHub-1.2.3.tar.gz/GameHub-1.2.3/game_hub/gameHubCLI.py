"""
holds all commands
"""
import click
from click_repl import repl
from prompt_toolkit.history import FileHistory
from pathlib import Path

from pyfiglet import Figlet

from game_hub.utils.logging import MyLogger

from game_hub import gameHub
from game_hub.games import gameCLI

logger = MyLogger.logging.getLogger('gamehub.gameHubCLI')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli() -> None:
    """
    gamehub is an interface for the three games we currently have in stock, which are tictactoe, hangman and rock paper
    scissors. You can play these games by typing 'gamehub play [game]' you can see the names of the games by typing in
    'gamehub play'. If you are in the repl, the commands are the same but you don't include the gamehub. As well as this
    , in the repl, you can press the tab key and a list of options appears that you can pick from.
    """
    pass


@cli.command('generate', short_help="pick random game to play")
def click_generate() -> None:
    """
    Pick Random Game to play
    """
    gameHub.generate()()


@cli.command("last_game", short_help="plays the last game you played")
def play_again() -> None:
    """
    plays the last game you played
    """
    gameHub.play_again(Path.home() / '.gameHub/lastGame.json')


@cli.command("play_list", short_help="play's a random game from a list")
@click.option('--games', '-g', nargs=1, type=str, help="type -g or --games + a game and repeat to make list",
              multiple=True)
def play_from_list(games) -> None:
    """
    play's a random game from a list and prints the closest command if you misspell it.
    \f
    :param games: string will print
    """
    games = list(games)
    picked_game = gameHub.play_random_game_from_list(games)
    if picked_game not in gameHub.cmd_name_to_game_name.values():
        logger.info(picked_game)
    else:
        gameHub.convert_str_to_game_func[picked_game]()


@cli.command('repl', short_help="creates a repl and a exit command")
def create_repl() -> None:
    """
    creates a repl and a exit command
    """
    f = Figlet(font='larry3d')
    logger.info(f.renderText('gamehub'))

    @cli.command("exit", short_help="breaks you out of repl")
    def exit_repl() -> None:
        """
        breaks you out of repl
        """
        raise EOFError

    cli.add_command(exit_repl)
    command_history_file = gameHub.gamehub_directory / 'system/my_repl_history'
    command_history_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_kwargs = {
        'history': FileHistory(command_history_file),
    }
    repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)


cli.add_command(gameCLI.play)
