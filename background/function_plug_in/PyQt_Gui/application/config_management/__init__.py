# -*- coding: utf-8 -*-
# @Time : 2024/7/22 下午2:45
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : __init__.py.py
# @Project : mc_auto_boss

from config import config
from function_plug_in import root_file
from function_plug_in.PyQt_Gui.application.config_management.model.config import ConfigModel

# 构建文件路径
VERSION_PATH = root_file('background/version.py')
EXAMPLE_PATH = root_file('echo_config.yaml')
CONFIG_PATH = root_file('config.yaml')

mc_cfg = ConfigModel(VERSION_PATH, EXAMPLE_PATH, CONFIG_PATH)
mc_cfg.game_path = config.AppPath
