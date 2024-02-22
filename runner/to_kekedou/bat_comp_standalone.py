# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/14 16:39
"""

import glob
import os
import sys
import shutil

sys.path.append("W:/projects/nzt/misc/users/yangtao/main_code")

from batch_repair import comp_collector

os.environ["MAYA_LOCATION"] = "C:/Program Files/Autodesk/Maya2019"
# os.environ["PYTHONPATH"] = "C:/Program Files/Autodesk/Maya2019/Python/Lib/site-packages"

sys.path.append("C:/Program Files/Autodesk/Maya2019/bin")
sys.path.append("C:/Program Files/Autodesk/Maya2019/plug-ins/ATF/scripts")
sys.path.append("C:/Program Files/Autodesk/Maya2019/plug-ins/MASH/scripts")
sys.path.append("C:/Program Files/Autodesk/Maya2019/plug-ins/fbx/scripts")
sys.path.append("C:/Program Files/Autodesk/Maya2019/plug-ins/camd/scripts")
sys.path.append("C:/Program Files/Autodesk/Maya2019/plug-ins/substance/scripts")
sys.path.append("C:/Program Files/Autodesk/Maya2019/plug-ins/xgen/scripts")
sys.path.append("C:/Program Files/Autodesk/Maya2019/bin/python27.zip")
sys.path.append("C:/Program Files/Autodesk/Maya2019/Python/DLLs")
sys.path.append("C:/Program Files/Autodesk/Maya2019/Python/lib")
sys.path.append("C:/Program Files/Autodesk/Maya2019/Python/lib/plat-win")
sys.path.append("C:/Program Files/Autodesk/Maya2019/Python/lib/lib-tk")
sys.path.append("C:/Program Files/Autodesk/Maya2019/bin")
sys.path.append("C:/Program Files/Autodesk/Maya2019/Python")
sys.path.append("C:/Program Files/Autodesk/Maya2019/Python/lib/site-packages")

import maya.standalone as standalone

import maya.cmds as mc
import maya.mel as mel

standalone.initialize(name="python")


def generate_comp(shot_file):
    print(shot_file)
    if os.path.exists(shot_file):
        mc.file(shot_file, open=True, prompt=False, ignoreVersion=True, f=True)
        d = comp_collector.Dialog("nzt")
        print(d.version_dir)

        comp_collector.generate_comp("nzt")


if __name__ == '__main__':
    ma_file = os.environ.get("MA_FILE", None)
    if not ma_file:
        ma_file = sys.argv[1]

    meow = """


          |\      _,,,---,,_
    ZZZzz /,`.-'`'    -.  ;-;;,_
         |,4-  ) )-,_. ,\ (  `'-'
        '---''(_/--'  `-'\_)  [File]: %s 


            """ % ma_file
    print(meow)

    generate_comp(ma_file)
