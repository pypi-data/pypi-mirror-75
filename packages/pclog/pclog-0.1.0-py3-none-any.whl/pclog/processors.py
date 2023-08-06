"""
Preprocessors collection.
"""
# pylint: disable=too-many-ancestors,too-few-public-methods

import logging
from typing import Optional, Any
from pprint import pformat

from .core import SingletonMeta, ChildsTreeMixin
from .settings import CFG
from .pyg import Pyg


class Checks(metaclass=SingletonMeta):
    """Checks for FormatProc"""
    is_colored: bool = True
    is_args_empty: Optional[bool] = None

    def update(self, record: logging.LogRecord) -> None:
        """Updating checks."""
        for check in dir(self):
            if check.startswith('_check_'):
                getattr(self, check)(record)

    def _check_args_empty(self, record: logging.LogRecord) -> bool:
        """Is record.args is empty?"""
        self.is_args_empty = not record.args
        return self.is_args_empty


class Proc(ChildsTreeMixin):
    """Applying changes to LogRecord"""
    checks = Checks()

    def __call__(self, record: logging.LogRecord) -> logging.LogRecord:
        """Calling self and childs process."""
        record = self.format(record)
        for child in self._childs_list:
            record = child.__call__(record)
        return record

    def format(self, record: logging.LogRecord) -> logging.LogRecord:
        """Applying changes to LogRecord"""
        if self.checks.is_args_empty:  # TODO: is msg as args?
            record.msg = self.format_item(record.msg)
        else:
            record = self.format_args(record)
        return record

    def format_args(self, record: logging.LogRecord) -> logging.LogRecord:
        """Applying changes to args tuple."""
        record.args = tuple([
            self.format_item(a) for a in record.args
        ])
        return record

    @staticmethod
    def format_item(item: Any) -> Any:
        """Applying changes to abstract item."""
        return item

    def exception(self, trace_info: str) -> str:
        """Calling childs for traceback processing."""
        for child in self._childs_list:
            trace_info = child.exception(trace_info)
        return trace_info


class LogLevelTab(Proc):
    """Log level tabulation."""
    log_levels_tab = {10: 3, 20: 4, 30: 1, 40: 3, 50: 0}

    def format(self, record: logging.LogRecord) -> logging.LogRecord:
        """Formatting lolevel str"""
        spaces: int = self.log_levels_tab[record.levelno]
        record.levelname = '{}{}'.format(record.levelname, ' '*spaces)
        return record


class Pformat(Proc):
    """Pprint formatter."""
    @staticmethod
    def format_item(item: Any) -> str:
        """Formatting single item."""
        if not isinstance(item, str):
            return pformat(item, compact=False, width=80)
        return item


class ToStr(Proc):
    """Args to string formatter."""
    @staticmethod
    def format_item(item: Any) -> str:
        """Formatting single item."""
        return str(item)


class ProcColor(ToStr):  # pylint: disable=abstract-method
    """Abstract class for colorization."""


class MessageColor(ProcColor):
    """Colors for message."""
    color = CFG.msg_color
    color_reset = CFG.reset_color

    def format(self, record: logging.LogRecord) -> logging.LogRecord:
        """Applying changes to LogRecord"""
        if not self.checks.is_args_empty:
            record.msg = self.format_item(record.msg)
        return record

    def format_item(self, item: str) -> str:  # type: ignore
        """Formatting item"""
        return '{}{}{}'.format(self.color, item, self.color_reset)


class LogLevelColor(ProcColor):
    """Log level colorization."""
    log_levels_fmt = CFG.log_levels_color

    def format(self, record: logging.LogRecord) -> logging.LogRecord:
        """Formatting lolevel str"""
        fmt: str = self.log_levels_fmt[record.levelno]
        record.levelname = fmt.format(record.levelname)
        return record


class ProcPygments(ProcColor):
    """Abstract class for pygments colorization."""


class ArgsPygments(ProcPygments):
    """Args colorization with pygments."""
    pyg: Pyg = Pyg()
    color_bg: str = CFG.pygments.color_bg
    lexer: str = CFG.pygments.lexer
    style: str = CFG.pygments.style

    def format_item(self, item: str) -> str:  # type: ignore
        """Formatting single item."""
        colored: str = self.pyg.build_hl(
            self.color_bg, self.lexer, self.style
        )(item)
        if colored.endswith('\n'):
            return colored[:-1]
        return colored


class NewlinedPformat(ToStr):
    """Start multilined data with newline."""
    # TODO: Parse msg, without changing data.
    @staticmethod
    def format_item(item: Any) -> Any:
        """Formatting single item."""
        if isinstance(item, str):
            if '\n' in item:
                return f'\n{item}'
        return item


class ArgsDefaultColor(ProcColor):
    """Colors for arguments."""
    color = CFG.args_color
    color_reset = CFG.msg_color

    def format_item(self, item: str) -> str:  # type: ignore
        """Formatting single item."""
        return '{}{}{}'.format(self.color, item, self.color_reset)


class ProcTraceback(ProcPygments):
    """Abstract class for traceback colorization."""
    @staticmethod
    def format(record: logging.LogRecord) -> logging.LogRecord:
        """Formatting lolevel str"""
        return record


class TracebackPygments(ProcTraceback):
    """Traceback colorization with pygments."""
    pyg: Pyg = Pyg()
    color_bg: str = CFG.pygments.color_bg
    lexer: str = CFG.pygments.tb_lexer
    style: str = CFG.pygments.tb_style

    def exception(self, trace_info: str) -> str:
        """Formatting traceback by pygments."""
        colored: str = self.pyg.build_hl(
            self.color_bg, self.lexer, self.style
        )(trace_info)
        if colored.endswith('\n'):
            return colored[:-1]
        return colored
