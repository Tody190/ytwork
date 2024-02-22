# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/24 16:42
"""


p = "W:/projects/nzt/misc/users/yangtao/main_code"
import sys

p in sys.path or sys.path.append(p)

from runner.bil import bat_render

bat_render.run()
