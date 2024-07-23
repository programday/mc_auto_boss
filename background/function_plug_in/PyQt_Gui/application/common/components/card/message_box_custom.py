# -*- coding: utf-8 -*-
# @Time : 2024/7/22 下午2:23
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : message_box_custom.py
# @Project : mc_auto_boss

import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel
from qfluentwidgets import MessageBox, ComboBox


class MessageBoxInstance(MessageBox):
    def __init__(self, title: str, content: dict, configtemplate: str, parent=None):
        super().__init__(title, "", parent)
        self.content = content

        self.textLayout.removeWidget(self.contentLabel)
        self.contentLabel.clear()

        self.yesButton.setText('确认')
        self.cancelButton.setText('取消')

        self.buttonGroup.setMinimumWidth(480)

        font = QFont()
        font.setPointSize(14)

        with open(configtemplate, 'r', encoding='utf-8') as file:
            self.template = json.load(file)

        self.comboBox_dict = {}
        for type, names in self.template.items():
            titleLabel = QLabel(type, parent)
            titleLabel.setFont(font)
            self.textLayout.addWidget(titleLabel, 0, Qt.AlignTop)

            comboBox = ComboBox()

            has_default = False
            for name, info in names.items():
                item_name = f"{name}（{info}）"
                comboBox.addItem(item_name)
                if self.content[type] == name:
                    comboBox.setCurrentText(item_name)
                    has_default = True
            if not has_default:
                comboBox.setText(self.content[type])

            self.textLayout.addWidget(comboBox, 0, Qt.AlignTop)
            self.comboBox_dict[type] = comboBox

        self.titleLabelInfo = QLabel("说明：清体力是根据选择的副本类型来判断的,\n此处设置的副本名称也会用于完成活动或每日实训对应的任务,\n如果即使有对应的任务,你也不希望完成,可以将对应的副本名称改为“无”", parent)
        self.textLayout.addWidget(self.titleLabelInfo, 0, Qt.AlignTop)
