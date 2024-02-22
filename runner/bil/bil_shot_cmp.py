# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/21 10:47
"""
import os.path
import subprocess

import maya.cmds as mc

import project_files

reload(project_files)
from batch_repair import comp_collector


def run():
    shots_geo = project_files.get_projcet_files("bil", contains=".ani.animation")

    shots_geo = sorted(shots_geo)

    for s_g in shots_geo:

        shot_name = os.path.basename(s_g).split(".")[0]

        if shot_name in ["n10010"]:
            continue

        print("------------------")
        print(shot_name, ":", s_g)
        print("------------------")

        mc.file(s_g,
                open=True,
                prompt=False,
                ignoreVersion=True,
                f=True)

        mc.currentUnit(t="30fps")

        comp_collector.generate_comp("bil")

        # version = project_files.pub_file_get_version("bil", s_g)
        # if version:
        #     cmd = 'rez-env oct_cache_exporter -- version_to_deadline %s' % str(version["id"])
        #     p = subprocess.Popen(cmd)
        #     p.wait()