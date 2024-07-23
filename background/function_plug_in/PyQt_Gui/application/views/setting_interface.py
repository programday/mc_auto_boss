# -*- coding: utf-8 -*-
# @Time : 2024/7/19 上午10:22
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : setting_interface.py
# @Project : mc_auto_boss
from typing import List

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel, QSpacerItem, QFileDialog
from qfluentwidgets import FluentIcon as FIF, PrimaryPushSettingCard, PushSettingCard
from qfluentwidgets import ScrollArea, Pivot, SettingCardGroup

from function_plug_in import application_file
from function_plug_in.PyQt_Gui.application.common.components.card.push_setting_card_instance import PushSettingCardInstance
from function_plug_in.PyQt_Gui.application.common.gui.style_sheet import StyleSheet
from function_plug_in.PyQt_Gui.application.config_management import mc_cfg


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 保存父对象
        self.parent = parent
        # 设置滚动区域，垂直布局，可以滚动查看所有控件
        self.scroll_widget = QWidget()
        self.v_box_layout = QVBoxLayout(self.scroll_widget)

        self.pivot = Pivot(self)
        self.stacked_widget = QStackedWidget(self)
        self.setting_label = QLabel(self.tr("设置"), self)

        self.__init_widget()
        self.__init_card()
        self.__init_layout()
        self.__connect_signal_to_slot()

    def __init_widget(self):
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 140, 0, 5)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setObjectName('settingInterface')
        self.scroll_widget.setObjectName('scroll_widget')
        self.setting_label.setObjectName('setting_label')
        StyleSheet.SETTING_INTERFACE.apply(self)

    def __init_card(self):
        self.combat_set_group = SettingCardGroup(self.tr("战斗"), self.scroll_widget)
        self.procedure_group = SettingCardGroup(self.tr("程序"), self.scroll_widget)
        self.about_group = SettingCardGroup(self.tr("关于"), self.scroll_widget)

        self.boos_instance_type_card = PushSettingCardInstance(
            "修改",
            FIF.PALETTE,
            self.tr('目标BOSS配置 (注意：在配置的BOSS处放好错位信标)'),
            'boss_name',
            application_file(r'./config_management/resource/boss_name.json'),
        )
        self.combat_strategy_type_card = PushSettingCardInstance(
            "修改",
            FIF.PALETTE,
            self.tr('攻击配置'),
            'combat_strategy',
            application_file(r'./config_management/resource/combat_strategy.json'),
        )
        self.github_card = PrimaryPushSettingCard(
            self.tr('项目主页'),
            FIF.GITHUB,
            self.tr('项目主页'),
            "https://github.com/lazydog28/mc_auto_boss"
        )

        self.game_path_card = PushSettingCard(
            self.tr('修改'),
            FIF.GAME,
            self.tr("游戏路径"),
            mc_cfg.game_path
        )

        self.qq_group_card = PrimaryPushSettingCard(
            self.tr('加入群聊'),
            FIF.EXPRESSIVE_INPUT_ENTRY,
            self.tr('QQ群'),
            "689545101"
        )
        self.feedback_card = PrimaryPushSettingCard(
            self.tr('提供反馈'),
            FIF.FEEDBACK,
            self.tr('提供反馈'),
            self.tr('帮助我们改进 March7thAssistant')
        )
        # self.about_card = PrimaryPushSettingCard(
        #     self.tr('检查更新'),
        #     FIF.INFO,
        #     self.tr('关于'),
        #     self.tr('当前版本：') + " " + mc_cfg.version
        # )

    @staticmethod
    def add_setting_card(group: SettingCardGroup, card_list: List[QWidget]):
        for card in card_list:
            group.addSettingCard(card)

    def __init_layout(self):
        self.setting_label.move(36, 30)
        self.pivot.move(40, 80)
        # self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignTop)
        self.v_box_layout.addWidget(self.stacked_widget, 0, Qt.AlignTop)
        self.v_box_layout.setContentsMargins(36, 0, 36, 0)
        self.add_setting_card(self.combat_set_group, [self.boos_instance_type_card, self.combat_strategy_type_card])

        self.add_sub_interface(self.combat_set_group, "combat_set_group", self.tr("战斗"))
        self.add_sub_interface(self.procedure_group, "procedure_group", self.tr("程序"))
        self.add_sub_interface(self.about_group, "about_interface", self.tr("关于"))

    @staticmethod
    def __open_url(url):
        return lambda: QDesktopServices.openUrl(QUrl(url))

    def __connect_signal_to_slot(self):
        """
        连接到槽函数

        """
        # 修改游戏路径
        self.game_path_card.clicked.connect(self.__on_game_path_card_clicked)

        # github
        self.github_card.clicked.connect(self.__open_url("https://github.com/lazydog28/mc_auto_boss"))
        # qq
        self.qq_group_card.clicked.connect(self.__open_url(""))
        # 提点建议
        self.feedback_card.clicked.connect(self.__open_url("https://github.com/lazydog28/mc_auto_boss/issues"))
        # 检查更新
        # self.about_card.clicked.connect(lambda: checkUpdate(self.parent))

    # noinspection PyUnresolvedReferences
    def add_sub_interface(self, widget: SettingCardGroup, objectName, text):
        def remove_spacing(layout):
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item, QSpacerItem):
                    layout.removeItem(item)
                    break

        remove_spacing(widget.vBoxLayout)
        widget.titleLabel.setHidden(True)

        widget.setObjectName(objectName)
        self.stacked_widget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stacked_widget.setCurrentWidget(widget)
        )

    def __on_game_path_card_clicked(self):
        game_path, _ = QFileDialog.getOpenFileName(self, "选择游戏路径", "", "All Files (*)")
        if not game_path or mc_cfg.game_path == game_path:
            return
        mc_cfg.set_value("AppPath", game_path)
        self.game_path_card.setContent(game_path)
