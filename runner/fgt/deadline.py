# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/22 23:17
"""



import os
import subprocess

cmd = 'rez-env oct_cache_exporter -- version_to_deadline %s' % str("207049")
p = subprocess.Popen(cmd)
p.wait()
