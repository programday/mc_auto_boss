# -*- coding: utf-8 -*-
# @Time : 2024/7/16 下午6:20
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : run_mc_auto_boss_gui.py
# @Project : mc_auto_boss
import os
import sys

from qfluentwidgets import FluentTranslator

from function_plug_in.PyQt_Gui.application.resource.common.config import cfg

# 将当前工作目录设置为程序所在的目录，确保无论从哪里执行，其工作目录都正确设置为程序本身的位置，避免路径错误。
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from function_plug_in.PyQt_Gui.application.main_window import McMainWindow

# 启用 DPI 缩放
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)

    w = McMainWindow()
    w.show()
    app.exec_()
