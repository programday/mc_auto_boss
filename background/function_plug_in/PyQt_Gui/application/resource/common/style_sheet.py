# -*- coding: utf-8 -*-
# @Time : 2024/7/17 上午11:13
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : style_sheet.py.py
# @Project : PyQt_Gui

from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    LINK_CARD = "link_card"
    SAMPLE_CARD = "sample_card"
    HOME_INTERFACE = "home_interface"
    ICON_INTERFACE = "icon_interface"
    VIEW_INTERFACE = "view_interface"
    SETTING_INTERFACE = "setting_interface"
    GALLERY_INTERFACE = "gallery_interface"
    NAVIGATION_VIEW_INTERFACE = "navigation_view_interface"

    Tutorial_INTERFACE = "tutorial_interface"
    HELP_INTERFACE = "help_interface"
    CHANGELOGS_INTERFACE = "changelogs_interface"
    WARP_INTERFACE = "warp_interface"
    TOOLS_INTERFACE = "tools_interface"

    def path(self, theme=Theme.AUTO):
        # qs
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/resource/qss/{theme.value.lower()}/{self.value}.qss"
