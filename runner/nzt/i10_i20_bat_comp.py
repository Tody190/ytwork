# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/25 17:09
"""
import glob
import os
import shutil

import maya.cmds as mc

import project_files
from batch_repair import comp_collector

from missions import MissionsPlanner


def build_mission():
    mission_path = "W:/projects/nzt/misc/users/yangtao/output/i20_comp_mission"

    mp = MissionsPlanner(mission_path)

    project_name = "NZT"
    seq_list = ["i20"]
    task_name = ".ani.animation"
    # output_path = "W:/projects/nzt/misc/users/yangtao/output/files_collection"

    all_shot_files = []

    for seq in seq_list:
        shot_files = project_files.get_projcet_files(project_name=project_name,
                                                     contains=task_name,
                                                     shot_start_with=seq)
        all_shot_files += shot_files

    for shot_file in all_shot_files:
        mp.create_missions(mission_name=os.path.basename(shot_file),
                           python_script=__file__,
                           fun_name="generate_comp",
                           fun_args=[shot_file]
                           )


def generate_comp(shot_file):
    print(shot_file)
    mc.file(shot_file, open=True, prompt=False, ignoreVersion=True, f=True)
    d = comp_collector.Dialog("nzt")
    print(d.version_dir)

    comp_collector.generate_comp("nzt")


def back_up_comp_json():
    project_name = "NZT"
    seq_list = ["i20"]
    task_name = ".ani.animation"
    output_path = "W:/projects/nzt/misc/users/yangtao/shot_components"

    all_shot_files = []

    for seq in seq_list:
        shot_files = project_files.get_projcet_files(project_name=project_name,
                                                     contains=task_name,
                                                     shot_start_with=seq)
        all_shot_files += shot_files

    for shot_file in all_shot_files:
        orig_comp_json = os.path.join(os.path.dirname(shot_file), "shot_components.json")
        if os.path.exists(orig_comp_json):
            version_name = os.path.basename(shot_file)
            dst_comp_json = os.path.join(output_path, "%s.json" % version_name)
            shutil.copy2(orig_comp_json, dst_comp_json)


def back_up_ma():
    project_name = "NZT"
    seq_list = ["i20"]
    task_name = ".ani.animation"
    output_path = "W:/projects/nzt/misc/users/yangtao/i20_bk"

    all_shot_files = []

    for seq in seq_list:
        shot_files = project_files.get_projcet_files(project_name=project_name,
                                                     contains=task_name,
                                                     shot_start_with=seq)
        all_shot_files += shot_files

    for shot_file in all_shot_files:
        dst_comp_json = os.path.join(output_path, "%s.ma" % os.path.basename(shot_file))
        print(shot_file, dst_comp_json)
        shutil.copy2(shot_file, dst_comp_json)



if __name__ == '__main__':
    build_mission()
    #back_up_comp_json()
    #back_up_ma()