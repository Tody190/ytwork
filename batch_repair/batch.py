# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/9 23:05
"""
import os.path

import maya.cmds as cmds
import maya.utils as mu

import project_files

reload(project_files)
import replace_references
reload(replace_references)

import playblast
reload(playblast)

from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path

project_name = "NZT"

replace_map = (("I:/projects/nzt/asset/asb/MiLin_ShangY/mod/MiLin_ShangY.mod.model/MiLin_ShangY.ma",
                "I:/projects/nzt/asset/asb/s076001woods/mod/s076001woods.mod.model/s076001woods.ma"),
               ("I:/projects/nzt/asset/asb/s075001deeppool/mod/s075001deeppool.mod.model/s075001deeppool.ma",
                "I:/projects/nzt/asset/asb/s076001woods/mod/s076001woods.mod.model/s076001woods.ma"))


def run(shot_name):
    print(shot_name)
    geo_file = project_files.get_ani_file_from_shot(project_name, shot_name)
    if not os.path.exists(geo_file):
        return
    print(geo_file)
    unlock_path(geo_file)

    # cmds.file(geo_file, open=True, f=True)

    for rf in replace_map:
        replace_references.replace_asset(rf[0], rf[1])

    preview_file = project_files.get_preview_file_from_shot(project_name, shot_name)
    print(preview_file)

    if os.path.exists(preview_file):
        unlock_path(preview_file)
        os.remove(preview_file)

    playblast.run(preview_file)


def batch_playblast(seq_name, output_dir):
    shots_file = project_files.get_projcet_files(project_name,
                                                 shot_start_with=seq_name,
                                                 contains="ani.animation")

    for f in shots_file:
        print("----------------------------")
        print(f)
        print("----------------------------")
        try:
            mov_file = output_dir + "/" + os.path.splitext(os.path.basename(f))[0] + ".mov"
            if not os.path.exists(mov_file):
                cmds.file(f, open=True, f=True)
                # for rf in replace_map:
                #     replace_references.replace_asset(rf[0], rf[1])
                playblast.run(mov_file, 2048, 1080)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    batch_playblast("i10", "W:/temp/batch_playblast/i10")
