# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/10/9 17:00
"""


p = "Z:/OCT/TEC/yangtao/main_code"

import sys

p in sys.path or sys.path.append(p)
from runner.to_kekedou import all_to_kekedou

ma_file = "I:/projects/nzt/shot/n80/n80380/ani/n80380.ani.blocking.v017/n80380.ani.blocking.v017.ma"
all_to_kekedou.single_to_kekedou(ma_file)