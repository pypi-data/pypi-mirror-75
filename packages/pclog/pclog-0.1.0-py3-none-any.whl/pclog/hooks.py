"""
Advanced Python hooks.
"""

import sys
import logging
import threading
import multiprocessing
from types import TracebackType
from typing import Type, Union


def traceback_to_log() -> None:
    """Pass native traceback to Logger"""
    def sys_hook(exc_type: type, exc_value: BaseException,
                 exc_traceback: TracebackType) -> None:
        logging.critical(
            '%s %s', multiprocessing.current_process().name,
            threading.current_thread().name,
            exc_info=(exc_type, exc_value, exc_traceback))

    def thread_for_py37(obj: Union[Type[threading.Thread],
                                   Type[multiprocessing.context.Process]]
                        ) -> None:
        """
        Workaround for sys.excepthook thread bug
        From https://bugs.python.org/issue1230540

        Call once from __main__ before creating any threads.
        If using psyco, call psyco.cannotcompile(threading.Thread.run)
        since this replaces a new-style class method.
        """
        # pylint: disable=protected-access
        def init(self, *args, **kwargs):  # type: ignore
            """Init hook."""
            def run_with_except_hook(*args, **kw):  # type: ignore
                """Run with except hook."""
                try:
                    run_old(*args, **kw)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:  # pylint: disable=bare-except
                    sys.excepthook(*sys.exc_info())

            init_old(self, *args, **kwargs)
            run_old = self.run
            self.run = run_with_except_hook

        init_old = obj.__init__
        obj.__init__ = init  # type: ignore

    sys.excepthook = sys_hook
    if sys.version_info >= (3, 8):
        threading.excepthook = sys_hook
        thread_for_py37(multiprocessing.Process)
    else:
        thread_for_py37(threading.Thread)
        thread_for_py37(multiprocessing.Process)
