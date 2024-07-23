# -*- coding: utf-8 -*-
# @Time : 2024/7/17 下午6:05
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : translator.py.py
# @Project : mc_auto_boss
from PyQt5.QtCore import QObject
from tasks.base.tasks import start_task

from function_plug_in.PyQt_Gui.application.programme_models.basic_input_view.model import BasicInputView


class BasicInputViewTranslator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.views = {
            'brush_boos': BasicInputView(title='刷boos', action=lambda: start_task("main"), icon="./application/resource/images/xiaoxiwang.jpg"),
            'compound_vo_sk': BasicInputView(title='合成声骸', action=lambda: start_task("main"), icon="./application/resource/images/xiaoxiwang.jpg"),
            'lock_vo_sk': BasicInputView(title='锁定声骸', action=lambda: start_task("main"), icon="./application/resource/images/xiaoxiwang.jpg"),
            'score_calculation_vo_sk': BasicInputView(title='得分计算', action=lambda: start_task("main"), icon="./application/resource/images/xiaoxiwang.jpg"),
            'stop_run': BasicInputView(title='停止运行', action=lambda: start_task("main"), icon="./application/resource/images/xiaoxiwang.jpg")
        }
