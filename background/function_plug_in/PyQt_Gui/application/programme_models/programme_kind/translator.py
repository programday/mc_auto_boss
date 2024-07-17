# coding: utf-8
from PyQt5.QtCore import QObject
from qfluentwidgets import FluentIcon as FIF

from function_plug_in.PyQt_Gui.application.programme_models.programme_kind.model import ProgrammeKind


class ProgrammeKindTranslatorModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.home = ProgrammeKind(name=self.tr('主页'), position=ProgrammeKind.Position.TOP, fluent_icon=FIF.HOME)
        self.course = ProgrammeKind(name=self.tr('教程'), position=ProgrammeKind.Position.TOP, fluent_icon=FIF.LIBRARY)
        self.common_problem = ProgrammeKind(name=self.tr('常见问题'), position=ProgrammeKind.Position.TOP, fluent_icon=FIF.QUESTION)
        self.update_log = ProgrammeKind(name=self.tr('更新日志'), position=ProgrammeKind.Position.BOTTOM, fluent_icon=FIF.HISTORY)
        self.setting = ProgrammeKind(name=self.tr('设置'), position=ProgrammeKind.Position.BOTTOM, fluent_icon=FIF.SETTING)
