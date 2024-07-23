# -*- coding: utf-8 -*-
# @Time : 2024/7/16 下午3:55
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : model.py
# @Project : mc_auto_boss

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (SplashScreen, SubtitleLabel, setFont, MSFluentWindow)

from function_plug_in.PyQt_Gui.application.common.gui.gui_config import cfg
from function_plug_in.PyQt_Gui.application.programme_models.programme_kind.translator import ProgrammeKindTranslatorModel
from function_plug_in.PyQt_Gui.application.views.help_interface import HelpInterface
from function_plug_in.PyQt_Gui.application.views.home_interface import HomeInterface
from function_plug_in.PyQt_Gui.application.views.setting_interface import SettingInterface


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class McMainWindow(MSFluentWindow):
    window_icon_path: str = './application/resource/images/xiaoxiwang.jpg'

    def __init__(self):
        super().__init__()
        """
        初始化
        
        """

        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.init_window()

        # create sub interface
        self.translator_model = ProgrammeKindTranslatorModel()
        self.translator_model.home.programme = HomeInterface(self)
        self.translator_model.course.programme = HelpInterface(self)

        self.translator_model.update_log.programme = Widget('更新', self)
        self.translator_model.setting.programme = SettingInterface(self)

        self.init_navigation()
        self.splash_screen.finish()

    def init_navigation(self):
        """
        添加导航项

        """
        # 接口列表
        interfaces = [
            self.translator_model.home,
            self.translator_model.course,
            self.translator_model.update_log,
            self.translator_model.setting,
        ]
        for interface in interfaces:
            # 注册板块
            self.addSubInterface(
                interface=interface.programme,
                position=interface.position,
                icon=interface.fluent_icon,
                text=interface.name
            )

        # 开启项目后，默认显示主页
        self.navigationInterface.setCurrentItem(self.translator_model.home.programme.objectName())

    def init_window(self):
        # 调整初始窗口大小
        self.resize(944, 680)
        self.setMinimumWidth(660)
        # 设置程序角标，启动界面
        self.setWindowIcon(QIcon(self.window_icon_path))
        # 设置程序标题
        self.setWindowTitle('mc_auto_boss')
        # 云母效果
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        # 启动画面
        self.splash_screen.setIconSize(QSize(106, 106))
        # 提升顶部
        self.splash_screen.raise_()
        # 获取桌面可用几何区域
        desktop = QApplication.desktop().availableGeometry()
        _w, _h = desktop.width(), desktop.height()
        # 移动窗口到屏幕中央
        self.move(_w // 2 - self.width() // 2, _h // 2 - self.height() // 2)
        self.show()
        # 处理挂起事件
        QApplication.processEvents()
