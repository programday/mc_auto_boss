# -*- coding: utf-8 -*-
# @Time : 2024/7/17 上午11:09
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : home_interface.py
# @Project : mc_auto_boss

import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from qfluentwidgets import ScrollArea

from ..programme_models.basic_input_view.translator import BasicInputViewTranslator
from ..resource.common.style_sheet import StyleSheet
from ..resource.components.card.sample_card_view import SampleCardView


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(436)

        self.v_box_layout = QVBoxLayout(self)
        self.gallery_label = QLabel('  天工宝库 \n mc_auto_boss', self)
        self.gallery_label.setStyleSheet("color: white;font-size: 30px; font-weight: 600;")
        self.gallery_label.setObjectName('gallery_label')
        self.v_box_layout.addWidget(self.gallery_label)

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # 阴影模糊半径
        shadow.setColor(Qt.black)  # 阴影颜色
        shadow.setOffset(1.2, 1.2)  # 阴影偏移量
        self.gallery_label.setGraphicsEffect(shadow)

        self.img = Image.open('./application/resource/images/Background 1.jpg')
        self.banner = None
        self.path = None

        self.v_box_layout.setContentsMargins(40, 30, 0, 0)
        self.v_box_layout.setSpacing(10)

        self.v_box_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # self.link_card_view = LinkCardView(self)
        # self.v_box_layout.addWidget(self.link_card_view, 1, Qt.AlignBottom)
        # self.link_card_view.add_card(
        #     FluentIcon.GITHUB,
        #     self.tr('GitHub repo'),
        #     self.tr('喜欢就给个星星吧\n拜托求求你啦|･ω･)'),
        #     "https://github.com/programday/mc_auto_boss",
        # )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        if not self.banner or not self.path:
            image_height = self.img.width * self.height() // self.width()
            crop_area = (0, 0, self.img.width, image_height)  # (left, upper, right, lower)
            cropped_img = self.img.crop(crop_area)
            img_data = np.array(cropped_img)  # Convert PIL Image to numpy array
            height, width, channels = img_data.shape
            bytes_per_line = channels * width
            self.banner = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888)
            path = QPainterPath()
            path.addRoundedRect(0, 0, width, height, 10, 10)  # 10 is the radius for corners
            self.path = path.simplified()

        painter.setClipPath(self.path)
        painter.drawImage(self.rect(), self.banner)


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.translator_model = BasicInputViewTranslator()

        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.v_box_layout = QVBoxLayout(self.view)

        self.__init_widget()
        self.load_samples()

    def __init_widget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.v_box_layout.setContentsMargins(0, 0, 0, 0)  # 设置内容边距为0
        self.v_box_layout.setSpacing(30)  # 设置控件间距为60
        self.v_box_layout.addWidget(self.banner)
        self.v_box_layout.setAlignment(Qt.AlignTop)

    def load_samples(self):
        basic_view = SampleCardView(self.tr("功能 >"), self.view)
        basic_view.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        for name, basic_input_view_translator in self.translator_model.views.items():
            # 添加功能板块
            basic_view.add_sample_card(
                icon=basic_input_view_translator.icon,
                title=basic_input_view_translator.title,
                action=basic_input_view_translator.action
            )

        self.v_box_layout.addWidget(basic_view)
