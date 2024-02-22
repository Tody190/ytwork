# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/1 14:32
"""
import os.path
import re

from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path


def clear_arnold(ma_file):
    with open(ma_file, "r") as f:
        data = f.readlines()
        print("read")
        flag = False
        for index in range(len(data)):
            line = data[index]
            if re.match("(.*)ai_subdiv_iterations(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_subdiv_type(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_translator(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_surface_shader(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_surface_shaderr(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_surface_shaderg(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_surface_shadeb(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_override(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_volume_shader(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_volume_shaderr(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_volume_shaderg(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)ai_volume_shaderb(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)aiAOVFilter(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)aiOptions(.*)", line):
                data[index] = ""
                flag = True
            if re.match("(.*)aiAOVDriver(.*)", line):
                data[index] = ""
                flag = True

    if flag:
        print("write!")
        with open(ma_file, "w") as f:
            f.writelines(data)


def clear_files(ma_files):
    for ma_f in ma_files:
        # unlock_path(ma_f)
        clear_arnold(ma_f)
        # lock_path(ma_f)


if __name__ == '__main__':
    ma_files = ["W:/projects/fgt/asset/prp/jgb_z90060/rig/maya/jgb_z90060.rig.rigging.v002.ma"]
    clear_files(ma_files)
