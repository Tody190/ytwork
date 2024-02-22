# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/6 23:24
"""
import os
import time


def run(t):
    time.sleep(t)
    print("")

def start():
    t = os.environ["sleep_time"]
    run(t)

run()