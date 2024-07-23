# -*- coding: utf-8 -*-
# @Time : 2024/7/22 下午5:57
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : game_controller.py
# @Project : mc_auto_boss
import os
from logging import Logger
from typing import Optional

from background.status import logger as status_logger


class GameController:
    def __init__(self, game_path: str, process_name: str, window_name: str, window_class: Optional[str], logger: Optional[Logger] = None) -> None:
        self.game_path = os.path.normpath(game_path)
        self.process_name = process_name
        self.window_name = window_name
        self.window_class = window_class
        self.logger = status_logger if logger is not None else logger
