"""
Settings module.
"""

from __future__ import annotations
from ast import literal_eval
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
from pkg_resources import resource_filename


@dataclass
class ConfPygments:
    """Pygments configuration."""
    color_bg: str
    lexer: str
    style: str
    tb_lexer: str
    tb_style: str


@dataclass(init=False)
class Config:
    """Primary configuration."""
    msg_color: str
    args_color: str
    reset_color: str
    log_levels_color: Dict[int, str]
    colors: Dict[str, str]
    pygments: ConfPygments
    config_file_name: str = 'conf/default.conf'

    def __init__(self) -> None:
        cfg_path = Path(
            resource_filename(__name__, self.config_file_name))

        with open(cfg_path, 'r') as file:
            cfg: Dict[str, Any] = literal_eval(
                file.read())

        self.update(cfg)

    def update(self, cfg: Dict[str, Any]) -> Config:
        """Update current config."""
        if 'colors' in cfg.keys():
            self.colors = cfg['colors']
        if 'pygments' in cfg.keys():
            self.pygments = ConfPygments(**cfg['pygments'])

        for i in ('msg', 'args', 'reset'):
            if i in cfg.keys():
                attr = f'{i}_color'
                val = self.colors[cfg[i]]
                setattr(self, attr, val)

        if 'log_levels' in cfg.keys():
            self.log_levels_color = {
                k: '{}{{}}{}'.format(self.colors[v], self.reset_color)
                for k, v in cfg['log_levels'].items()}

        return self


CFG = Config()
