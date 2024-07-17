# -*- coding: utf-8 -*-
# @Time : 2024/7/16 下午3:55
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : model.py
# @Project : mc_auto_boss
from typing import Optional

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from pydantic import ConfigDict, Field, BaseModel
from pydantic.dataclasses import dataclass
from qfluentwidgets import FluentIcon, NavigationItemPosition


@dataclass(config=ConfigDict(populate_by_name=True, arbitrary_types_allowed=True))
class ProgrammeKind:
    class Position:
        """
        板块位置
        """
        TOP = NavigationItemPosition.TOP
        SCROLL = NavigationItemPosition.SCROLL
        BOTTOM = NavigationItemPosition.BOTTOM

    programme: Optional[QWidget] = Field(None, title='板块')
    name: str = Field(title='板块名称')
    position: NavigationItemPosition = Field(Position.TOP, title='板块位置')
    fluent_icon: FluentIcon = Field(title='板块图标')
