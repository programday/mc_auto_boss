# -*- coding: utf-8 -*-
# @Time : 2024/7/18 上午10:13
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : help_interface.py
# @Project : mc_auto_boss
import os
import re
import sys
import traceback

import markdown
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel, QSpacerItem
from qfluentwidgets import ScrollArea, Pivot

from background.status import logger
from function_plug_in.PyQt_Gui.application.common.gui.style_sheet import StyleSheet


class HelpInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 滚动区域的主体
        self.scroll_widget = QWidget()
        # 垂直布局，用于排列 scroll_widget 内部子组件
        self.v_box_layout = QVBoxLayout(self.scroll_widget)
        # 用于导航和堆叠显示多个窗口部件
        self.pivot = Pivot(self)
        self.stacked_widget = QStackedWidget(self)
        # 帮助标签
        self.help_label = QLabel(self.tr("帮助"), self)
        self.help_label.setStyleSheet("font-size: 20px; font-weight: 510;")
        self.tutorial_label = QLabel(parent)
        self.common_problem_label = QLabel(parent)
        self.recommended_configuration_label = QLabel(parent)

        # self.update_log_label = QLabel(parent)

        self.__init_widget()
        self.__init_card()
        self.__init_layout()

    def __init_widget(self):
        # 设置滚动区域的主体
        self.setWidget(self.scroll_widget)
        # 允许滚动区域大小可调整
        self.setWidgetResizable(True)
        # 设置视口的边距
        self.setViewportMargins(0, 123, 0, 5)
        # 隐藏水平滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 设置对象名称用于样式应用
        self.setObjectName('HelpInterface')
        #
        self.scroll_widget.setObjectName('scroll_widget')
        self.help_label.setObjectName('help_label')
        # 应用样式表
        StyleSheet.HELP_INTERFACE.apply(self)

        # 确保 QLabel 支持富文本
        self.tutorial_label.setTextFormat(Qt.RichText)
        self.common_problem_label.setTextFormat(Qt.RichText)
        # self.update_log_label.setTextFormat(Qt.RichText)

    @staticmethod
    def open_url(url):
        QDesktopServices.openUrl(QUrl(url))

    def __init_card(self):
        # 教程
        tutorial_style = """
        <style>
        a {
            color: #009faa;
            font-weight: bold;
        }
        </style>
        """

        self.__add_card(self.tutorial_label, css_style=tutorial_style, base_path="./application/resource/doc/", md_name="GPU环境搭建.md")
        self.__add_card(self.common_problem_label, css_style=tutorial_style, base_path="./application/resource/doc/", md_name="common_problem.md")
        # self.__add_card(self.update_log_label, css_style=tutorial_style, base_path="./application/resource/doc/", md_name="GPU环境搭建.md")
        self.__add_card(self.recommended_configuration_label, css_style=tutorial_style, base_path="./application/resource/doc/", md_name="recommended_configuration.md")

    def __add_card(self, ql_abel: QLabel, css_style: str, base_path: str, md_name: str, ):
        try:
            with open(f"{base_path}/{md_name}", 'r', encoding='utf-8') as file:
                self.content = file.read()
                self.content = '\n'.join(self.content.split('\n')[1:])
                self.content = self.convert_relative_paths_to_absolute(self.content, base_path)
        except FileNotFoundError:
            for line in traceback.format_exc().split('\n'):
                logger(f'[打开文件异常]{line}', level='ERROR')
            sys.exit(1)
        tutorial_content = css_style + markdown.markdown(self.content).replace('<h2>', '<br><h2>').replace('</h2>', '</h2><hr>').replace('<br>', '', 1) + '<br>'
        ql_abel.setStyleSheet("""font-size: 16px;""")
        # 使处理好的文本可以打开外部链接
        ql_abel.setText(tutorial_content)
        ql_abel.setOpenExternalLinks(True)
        ql_abel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        # 将信号连接到open_url
        ql_abel.linkActivated.connect(self.open_url)

    # def __theme_changed(self):
    #     """
    #     更改主题样式
    #     """
    #     if qconfig.theme.name == "DARK":
    #         self.tasksLabel.setText(self.tasks_content.replace("border: 1px solid black;", "border: 1px solid white;"))
    #     else:
    #         self.tasksLabel.setText(self.tasks_content)

    def __init_layout(self):
        self.help_label.move(23, 30)
        self.pivot.move(40, 56)
        # self.v_box_layout.addWidget(self.pivot, 0, Qt.AlignTop)
        self.v_box_layout.addWidget(self.stacked_widget, 0, Qt.AlignTop)
        self.v_box_layout.setContentsMargins(26, 41, 36, 0)

        # self.vBoxLayout.addWidget(self.tutorialLabel, 0, Qt.AlignTop)
        self.add_sub_interface(self.tutorial_label, 'tutorial_label', self.tr('使用教程'))
        self.add_sub_interface(self.common_problem_label, 'common_problem_label', self.tr('常见问题'))
        # self.add_sub_interface(self.update_log_label, 'update_log_label', self.tr('更新日志'))
        self.add_sub_interface(self.recommended_configuration_label, 'recommended_configuration_label', self.tr('推荐游戏配置'))

        # currentChanged 信号连接到 onCurrentIndexChanged
        self.stacked_widget.currentChanged.connect(self.on_current_index_changed)
        # 切换控件对象名称
        self.pivot.setCurrentItem(self.stacked_widget.currentWidget().objectName())
        # 设置组件的固定高度为当前选中的子部件高度
        self.stacked_widget.setFixedHeight(self.stacked_widget.currentWidget().sizeHint().height())

    def on_current_index_changed(self, index):
        """
        设置槽函数，当stacked_widget变化时调用此函数
        同步导航控件 pivot 的选中项、重置垂直滚动条的位置，以及调整堆叠小部件的高度，以确保界面的一致性和良好的用户体验
        """

        widget = self.stacked_widget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        # 重置滚动条位置，将其设置为顶部
        self.verticalScrollBar().setValue(0)
        # 高度设置为建议高度
        self.stacked_widget.setFixedHeight(self.stacked_widget.currentWidget().sizeHint().height())

    def add_sub_interface(self, widget: QLabel, objectName, text):
        """
        添加子界面
        """

        def remove_spacing(layout):
            """
            删除间隔项
            """
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item, QSpacerItem):
                    layout.removeItem(item)
                    break

        # remove_spacing(widget.vBoxLayout)
        # widget.titleLabel.setHidden(True)

        widget.setObjectName(objectName)
        self.stacked_widget.addWidget(widget)
        # 添加导航项
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stacked_widget.setCurrentWidget(widget)
        )

    @staticmethod
    def convert_relative_paths_to_absolute(content, base_path):
        """
        返回绝对路径
        """
        pattern = re.compile(r'!\[.*?\]\((.*?)\)')
        matches = pattern.findall(content)
        for match in matches:
            if not match.startswith('http://') and not match.startswith('https://'):
                absolute_path = os.path.join(base_path, match)
                content = content.replace(match, absolute_path)
        return content
