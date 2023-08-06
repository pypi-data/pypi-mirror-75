"""
Examples.
"""

import logging
import logging.config
import threading
import multiprocessing
from typing import NoReturn, Dict
from . import Fmt


log: logging.Logger = logging.getLogger(__name__)

LOG_CONFIG: Dict = {
    'version': 1,
    'root': {'level': 'DEBUG',
             'handlers': ['stderr']},
    'loggers': {'__main__': {'propagate': True,
                             'handlers': ['drop']},
                'pclog': {'propagate': True,
                          'handlers': ['drop']}},
    'handlers': {'drop': {'class': 'logging.NullHandler'},
                 'stderr': {'class': 'logging.StreamHandler',
                            'level': 'DEBUG',
                            'formatter': 'long_color'}},
    'formatters': {'long_color': {
        '()': Fmt,
        'format': ('{orange}->{reset} '
                   '%(asctime)s %(levelname)s {white}<{reset}'
                   '%(filename)s:%(lineno)-3d{white}>{reset} '
                   '%(name)s.%(funcName)s{white}]:{reset} '
                   '%(message)s{reset}'),
        'datefmt': '%H:%M:%S',
        # 'config': {
        #     'msg': 'green',
        #     'log_levels': {
        #         10: 'green',
        #         20: 'blue',
        #         30: 'yellow',
        #         40: 'orange',
        #         50: 'green',
        #     },
        #     'pygments': {
        #         'color_bg': 'dark',
        #         'lexer': 'python3',
        #         'style': 'paraiso-dark',
        #         'tb_lexer': 'py3tb',
        #         'tb_style': 'native',
        #     },
        # },
    }}
}


def logger_create(config: dict) -> None:
    """Creating logger."""
    logging.config.dictConfig(config)


def bad_thread() -> NoReturn:
    """Thread exception test."""
    raise ZeroDivisionError('Test error.')


def bad_mp() -> NoReturn:
    """Multiprocessing exception test."""
    raise ZeroDivisionError('Test error.')


def messages_print() -> NoReturn:
    """Print log messages."""
    fake_data = [tuple(range(10)) for _ in range(5)]
    log.debug('Debug message: %s\nAdditional: %s', fake_data, fake_data)
    log.info(fake_data, extra={'cfg': {'test': 'OK'}})
    log.warning('Warn message: %s', dir(fake_data)[:10])
    log.error('Error message: %s %s', fake_data, fake_data)
    log.critical('Critical message: %s', tuple(fake_data))
    log.info('Stack', stack_info=True)
    try:
        threading.Thread(target=bad_thread).start()
    except ZeroDivisionError:
        pass
    try:
        multiprocessing.Process(target=bad_mp).start()
    except ZeroDivisionError:
        pass
    try:
        raise RuntimeError('Test error')
    except RuntimeError:
        log.exception('Exception log')
        raise


def main() -> None:
    """Start examples."""
    # stderr_tty = sys.stderr.isatty()
    # stdout_tty = sys.stdout.isatty()
    logger_create(LOG_CONFIG)
    messages_print()
