from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from qfluentwidgets import IconWidget, FlowLayout, CardWidget

from background.status import logger
from function_plug_in.PyQt_Gui.application.common.gui.style_sheet import StyleSheet


class SampleCard(CardWidget):
    """ Sample card """

    def __init__(self, icon, title, action, parent=None):
        super().__init__(parent=parent)

        self.action = action

        self.iconWidget = IconWidget(icon, self)
        self.iconOpacityEffect = QGraphicsOpacityEffect(self)
        self.iconOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.iconWidget.setGraphicsEffect(self.iconOpacityEffect)

        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: 500;")
        self.titleOpacityEffect = QGraphicsOpacityEffect(self)
        self.titleOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.titleLabel.setGraphicsEffect(self.titleOpacityEffect)
        # self.contentLabel = QLabel(TextWrap.wrap(content, 45, False)[0], self)

        self.hBoxLayout = QVBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedSize(130, 160)
        self.iconWidget.setFixedSize(110, 110)

        # self.hBoxLayout.setSpacing(28)
        # self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setSpacing(2)
        # self.v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget, alignment=Qt.AlignCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignCenter)
        # self.v_box_layout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        # self.contentLabel.setObjectName('contentLabel')

    # def showBottomTeachingTip(self):
    #     if not cfg.get_value(base64.b64decode("YXV0b191cGRhdGU=").decode("utf-8")):
    #         disclaimer(self)
    #     TeachingTip.create(
    #         target=self.iconWidget,
    #         icon=InfoBarIcon.SUCCESS,
    #         title='执行完成(＾∀＾●)',
    #         content="",
    #         isClosable=False,
    #         tailPosition=TeachingTipTailPosition.BOTTOM,
    #         duration=2000,
    #         parent=self
    #     )

    # def create_menu(self, pos):
    #     menu = RoundMenu(parent=self)
    #
    #     def create_triggered_function(task):
    #         def triggered_function():
    #             # self.showBottomTeachingTip()
    #             try:
    #                 task()
    #             except Exception as e:
    #                 logger(f"执行失败：{e}", level='ERROR')
    #
    #         return triggered_function
    #
    #     for index, (key, value) in enumerate(self.action.items()):
    #         menu.addAction(QAction(key, triggered=create_triggered_function(value)))
    #
    #         if index != len(self.action) - 1:  # 检查是否是最后一个键值对
    #             menu.addSeparator()
    #
    #     menu.exec(pos, ani=True)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if callable(self.action):
            # self.showBottomTeachingTip()
            try:
                self.action()
            except Exception as e:
                logger(f"执行失败：{e}", level='ERROR')
        # elif isinstance(self.action, dict):
        #     self.create_menu(e.globalPos())

    def enterEvent(self, event):
        super().enterEvent(event)
        self.iconOpacityEffect.setOpacity(0.75)
        self.titleOpacityEffect.setOpacity(0.75)
        self.setCursor(Qt.PointingHandCursor)  # 设置鼠标指针为手形

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.iconOpacityEffect.setOpacity(1)
        self.titleOpacityEffect.setOpacity(1)
        self.setCursor(Qt.ArrowCursor)  # 恢复鼠标指针的默认形状


class SampleCardView(QWidget):
    """ Sample card view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(10, 0, 40, 0)
        self.vBoxLayout.setSpacing(30)
        self.flowLayout.setContentsMargins(30, 0, 30, 0)
        self.flowLayout.setHorizontalSpacing(26)
        self.flowLayout.setVerticalSpacing(19)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName('viewTitleLabel')
        StyleSheet.SAMPLE_CARD.apply(self)

    def add_sample_card(self, icon, title, action):
        """ add sample card """
        card = SampleCard(icon, title, action, self)
        self.flowLayout.addWidget(card)
