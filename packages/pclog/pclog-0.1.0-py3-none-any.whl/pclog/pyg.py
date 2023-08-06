"""
Pygments processing.
"""

from functools import lru_cache, partial
from typing import Callable
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import (  # pylint: disable=no-name-in-module
    TerminalTrueColorFormatter)
from .core import SingletonMeta
# from pygments.styles import STYLE_MAP
# print(STYLE_MAP.keys())


class Pyg(metaclass=SingletonMeta):  # pylint: disable=too-few-public-methods
    """Pygments processor."""
    @staticmethod
    @lru_cache(maxsize=10)
    def build_hl(color_bg: str, lexer: str, style: str) -> Callable:
        """Building pygments highlighter."""
        lex = get_lexer_by_name(lexer, stripall=True)
        formatter = TerminalTrueColorFormatter(
            bg=color_bg, style=style, linenos=False)
        return partial(
            highlight, lexer=lex, formatter=formatter)
