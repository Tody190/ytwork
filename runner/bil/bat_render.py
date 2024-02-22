# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/24 15:15
"""

import os
import subprocess

import project_files


def run():
    shots_geo = project_files.get_projcet_files("bil", contains="ani.animation")

    shots_geo = sorted(shots_geo)

    for s_g in shots_geo:
        shot_name = os.path.basename(s_g).split(".")[0]
        version = project_files.pub_file_get_version("bil", s_g)
        if version:
            # if shot_name != "n10360":
            #     continue
            print(shot_name, version["sg_path_to_geometry"], str(version["id"]))
            cmd = 'rez-env oct_cache_exporter -- version_to_deadline %s' % str(version["id"])
            p = subprocess.Popen(cmd)
            p.wait()
