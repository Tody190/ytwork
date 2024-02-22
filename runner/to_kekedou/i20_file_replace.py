# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/14 14:56
"""
import glob
import os
import shutil
import time

import project_files
from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path


def backup_file(the_file):
    bak_file = the_file + ".bak"
    if os.path.exists(bak_file):
        print("backup exists %s" % bak_file)
        return

    time.sleep(1)

    parent_path = os.path.dirname(the_file)
    unlock_path(parent_path)
    shutil.copy(the_file, bak_file)
    lock_path(parent_path)
    lock_path(bak_file)


def replace_file(src_file, dst_file):
    print(src_file, "==>", dst_file)

    src_file_creation_time = os.path.getctime(src_file)
    dst_file_creation_time = os.path.getctime(dst_file)
    if src_file_creation_time == dst_file_creation_time:
        print("same time")
        return

    parent_path = os.path.dirname(dst_file)
    unlock_path(parent_path)
    unlock_path(dst_file)
    shutil.copy2(src_file, dst_file)
    lock_path(parent_path)
    lock_path(dst_file)


# 将之前替换过场景并拍屏的资产替换为新的
files_path = "W:/projects/nzt/misc/users/yangtao/output/i20"
maya_files = glob.glob(files_path + "/*.ma")
for local_file in maya_files:
    local_file_name = os.path.basename(local_file)
    #local_mov_name = local_file_name.replace(".ma", ".mov")
    local_preview_file = local_file.replace(".ma", ".mov")

    oct_shot_name = local_file_name.split(".")[0]
    oct_seq_name = oct_shot_name[:3]
    oct_step_name = local_file_name.split(".")[1]
    oct_task_name = local_file_name.split(".")[2]
    oct_contains = "%s.%s" % (oct_step_name, oct_task_name)

    # I:/projects/nzt/shot/i20/i20260/ani/i20260.ani.animation.v025/i20260.ani.animation.v025.ma
    pub_file = project_files.get_projcet_files("nzt", oct_contains, oct_shot_name)[0]
    pub_file_name = os.path.basename(pub_file)
    pub_mov_name = pub_file_name.replace(".ma", ".mov")  # i20260.ani.animation.v025.mov
    pub_components_file = os.path.dirname(pub_file) + "/shot_components.json"
    pub_preview_file = os.path.dirname(pub_file) + "/preview/" + pub_mov_name

    replace_file(local_file, pub_file)
    replace_file(local_preview_file, pub_preview_file)

    # print("Shot Name: ", oct_shot_name)
    # backup_file(pub_file)
    # print(pub_file)
    # backup_file(pub_preview_file)
    # print(pub_preview_file)
    # backup_file(pub_components_file)
    # print(pub_components_file)
