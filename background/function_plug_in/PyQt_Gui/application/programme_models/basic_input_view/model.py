# -*- coding: utf-8 -*-
# @Time : 2024/7/17 下午6:02
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : model.py
# @Project : mc_auto_boss
from typing import Optional

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass


@dataclass(config=ConfigDict(populate_by_name=True, arbitrary_types_allowed=True))
class BasicInputView:
    icon: Optional[str] = Field(None, title='图标')
    title: str = Field(title='功能名称')
    action: Optional[callable] = Field(None, title='功能行为')
