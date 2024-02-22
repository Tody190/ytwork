# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/11 9:53
"""
import os.path

from missions import MissionsPlanner
from missions import Quester
import project_files


def build_mission():
    output_dir = "W:/projects/nzt/misc/users/yangtao/output/i10"
    mission_path = output_dir + "/mission"

    shots_file = project_files.get_projcet_files("nzt",
                                                 shot_start_with="i10",
                                                 contains="ani.animation")
    mp = MissionsPlanner(mission_path)
    for file in shots_file:
        mp.create_missions(mission_name=os.path.basename(file),
                           python_script=__file__,
                           fun_name="run_mission",
                           fun_args=[file,
                                     output_dir]
                           )


def run_mission(maya_file, output_dir):
    # maya_file = os.environ.get("m_file")
    # output_dir = os.environ.get("m_output")

    print("maya_file: ", maya_file)
    print("output_dir: ", output_dir)

    import maya.cmds as cmds
    import sys

    p = "W:/projects/nzt/misc/users/yangtao/main_code"
    p in sys.path or sys.path.append(p)

    # from batch_repair import playblast
    from playblast import pb_main

    mov_file = output_dir + "/" + os.path.splitext(os.path.basename(maya_file))[0] + ".mov"
    print("mov_file: ", mov_file)

    cmds.file(maya_file, open=True, f=True)

    # 隐藏所有参考
    pb_main.organize_outline()
    # 适配帧范围
    shot_name = os.path.basename(maya_file).split(".")[0]
    pb_main.fit_frame_range("nzt", shot_name)

    pb_main.run(mov_file, width=2048, height=1080)


if __name__ == '__main__':
    build_mission()
