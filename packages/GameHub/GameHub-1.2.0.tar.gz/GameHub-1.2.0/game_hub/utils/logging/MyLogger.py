"""
Bonus:
- Make logs be pretty printed
"""
import os
import logging
import logging.config

from datetime import datetime
from pathlib import Path
from typing import Union


def configure_logger(name: str, log_path: Union[str, Path]) -> logging.Logger:
    """
    configures the logger
    """
    if isinstance(log_path, str):
        log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'message': {'format': '%(message)s'},
            'default': {'format': '%(asctime)s - %(name)-27s:[%(lineno)-4d] - function:%(funcName)-20s - '
                                  '%(levelname)-8s - %(message)s',
                        'datefmt': '%Y/%m/%d %I:%M:%S %p'}
        },
        'handlers': {
            'print_to_console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'message',
                'stream': 'ext://sys.stdout'
            },
            'log_to_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_path,
                'backupCount': 0
            },
            'root': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': os.path.splitext(str(log_path))[0] + '_root.log',
                'backupCount': 0
            }
        },
        'loggers': {
            name: {
                'level': 'DEBUG',
                'handlers': ['print_to_console', 'log_to_file'],
                'filemode': 'w'
            },
            '': {
                'level': 'DEBUG',
                'handlers': ['root'],
                'filemode': 'w'
            }
        }
    })
    return logging.getLogger(name)


logs_path = Path.home() / '.gameHub/system/logs/'
log_file = logs_path / f'gamehub_{datetime.today().date()}.log'
logger = configure_logger('gamehub', log_file)
