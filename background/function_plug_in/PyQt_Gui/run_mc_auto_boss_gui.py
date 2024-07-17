# -*- coding: utf-8 -*-
# @Time : 2024/7/16 下午6:20
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : run_mc_auto_boss_gui.py
# @Project : mc_auto_boss
import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from function_plug_in.PyQt_Gui.application.main_window import McMainWindow
from function_plug_in.PyQt_Gui.application.resource.common.config import cfg

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    galleryTranslator = QTranslator()
    # galleryTranslator.load(locale, "gallery", ".", ":/gallery/i18n")

    w = McMainWindow()
    w.show()
    app.exec_()
