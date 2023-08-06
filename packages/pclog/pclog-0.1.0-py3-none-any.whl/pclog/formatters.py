"""
Formatter module.
"""

import sys
import logging
from types import TracebackType
from typing import Optional, Union, Tuple, Dict
from .settings import CFG
from .processors import Proc, Checks
from . import hooks

# TODO: Add configuration from logging.conf


class CoreFormatter(logging.Formatter):
    """Core formatter functionality."""
    proc: Proc
    checks: Checks
    colors: Dict[str, str]

    def __init__(self,  # pylint: disable=too-many-arguments
                 fmt: Optional[str] = None,
                 datefmt: Optional[str] = None,
                 style: str = '%',
                 validate: bool = True,
                 # config: Optional[Dict[str, Any]] = None,
                 ) -> None:

        # if config is not None:
        #     CFG.update(config)
        self.checks = Checks()
        self.proc = Proc()
        self.colors = CFG.colors
        if fmt is not None:
            fmt = self.get_fmt(fmt)
        hooks.traceback_to_log()

        if sys.version_info >= (3, 8):
            super().__init__(fmt, datefmt, style, validate)
        else:
            super().__init__(fmt, datefmt, style)

    def get_fmt(self, fmt: str) -> str:
        """Parse fmt configuration string."""
        if self.checks.is_colored:
            return fmt.format(**self.colors)
        return fmt.format(**{color: '' for color in self.colors})

    def format(self, record: logging.LogRecord) -> str:
        self.checks.update(record)
        self.proc(record)
        return super().format(record)

    def formatException(self, ei: Union[
            Tuple[type, BaseException, Optional[TracebackType]],
            Tuple[None, None, None]]) -> str:
        trace_info: str = super().formatException(ei)
        trace_info = self.proc.exception(trace_info)
        return trace_info

    def formatStack(self, stack_info: str) -> str:
        return self.proc.exception(stack_info)
