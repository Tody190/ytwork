# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/14 17:26
"""

import subprocess

ma_f = "I:/projects/nzt/shot/i20/i20810/ani/i20810.ani.animation/i20810.ani.animation.v003.ma"
script_f = "W:/projects/nzt/misc/users/yangtao/main_code/runner/to_kekedou/bat_comp_standalone.py"
p = subprocess.Popen(
    'rez-env oct_maya maya-2019 maya_plugins -- mayapy %s %s' % (script_f, ma_f))
p.wait()
