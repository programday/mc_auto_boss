# -*- coding: utf-8 -*-
# @Time : 2024/7/22 下午2:21
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : push_setting_card_instance.py
# @Project : mc_auto_boss
import json
from typing import Union

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from qfluentwidgets import SettingCard, FluentIconBase

from function_plug_in.PyQt_Gui.application.common.components.card.message_box_custom import MessageBoxInstance
from function_plug_in.PyQt_Gui.application.config_management import mc_cfg


class PushSettingCard(SettingCard):
    """
    用于创建带有按钮和配置功能的设置卡片，并在按钮点击时弹出一个对话框来修改配置

    """
    clicked = pyqtSignal()

    def __init__(self, text, icon: Union[str, QIcon, FluentIconBase], title, config_name, config_value, parent=None):
        super().__init__(icon, title, config_value, parent)
        self.title = title
        self.config_name = config_name
        self.button = QPushButton(text, self)
        # 将按钮添加到水平布局中，并将其右对齐
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        # 在按钮和其他组件之间添加间距
        self.hBoxLayout.addSpacing(16)


class PushSettingCardInstance(PushSettingCard):
    """
    增加了配置模板的功能

    """

    def __init__(self, text, icon: Union[str, QIcon, FluentIconBase], title, config_name, config_template, parent=None):
        self.config_template = config_template
        with open(config_template, 'r', encoding='utf-8') as file:
            content = json.loads(file.read())
        self.config_value = mc_cfg.get_value(config_name, content)
        super().__init__(text, icon, title, config_name, str(self.config_value), parent)
        self.button.clicked.connect(self.__on_clicked)

    def __on_clicked(self):
        message_box = MessageBoxInstance(self.title, self.config_value, self.config_template, self.window())
        if message_box.exec():
            for _type, combobox in message_box.comboBox_dict.items():
                self.config_value[_type] = combobox.text().split('（')[0]
            mc_cfg.set_value(self.config_name, self.config_value)
            self.contentLabel.setText(str(self.config_value))
