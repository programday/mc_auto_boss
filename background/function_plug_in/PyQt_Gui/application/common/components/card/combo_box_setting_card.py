# -*- coding: utf-8 -*-
# @Time : 2024/7/19 上午11:03
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : combo_box_setting_card.py
# @Project : mc_auto_boss
from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from qfluentwidgets import (ComboBox, SettingCard, FluentIconBase)

from function_plug_in.PyQt_Gui.application.common import cfg


class ComboBoxSettingCard(SettingCard):
    """ Setting card with a combo box """

    def __init__(self, configname: str, icon: Union[str, QIcon, FluentIconBase], title, content=None, texts=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.configname = configname
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        for text, option in zip(texts, texts):
            self.comboBox.addItem(text, userData=option)

        self.comboBox.setCurrentText(cfg.get_value(configname))
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)

    def _onCurrentIndexChanged(self, index: int):
        cfg.set_value(self.configname, self.comboBox.itemData(index))
