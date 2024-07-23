# -*- coding: utf-8 -*-
# @Time : 2024/7/16 下午3:46
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File :
# @Project : mc_auto_boss

import os

# 定义插件根目录
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
APPLICATION_PATH = os.path.abspath(os.path.join(PROJECT_ROOT_PATH, 'background/function_plug_in/PyQt_Gui/application'))


def root_file(file_path):
    return os.path.abspath(os.path.join(PROJECT_ROOT_PATH, file_path))


def application_file(file_path):
    return os.path.abspath(os.path.join(APPLICATION_PATH, file_path))
