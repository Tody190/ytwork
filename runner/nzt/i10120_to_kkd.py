# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/25 15:51
"""
import sys

p = "W:/projects/nzt/misc/users/yangtao/main_code"
p in sys.path or sys.path.append(p)

import project_files
from coco_fils_process import to_kekedou

if __name__ == '__main__':
    project_name = "NZT"
    seq_list = ["i10"]
    task_name = ".ani.animation"
    output_path = "W:/projects/nzt/misc/users/yangtao/output/files_collection"

    all_shot_files = []

    for seq in seq_list:
        shot_files = project_files.get_projcet_files(project_name=project_name,
                                                     contains=task_name,
                                                     shot_start_with=seq)
        all_shot_files += shot_files

    for each_ma_file in all_shot_files:
        step = each_ma_file.split("/")[4]

        otk = to_kekedou.OCTToKEKEDOU(each_ma_file)
        otk.oct_to_kekedou(dst_dir=output_path, cover=True,
                           preview=True, components_json=True, translated_data=True,
                           source_images=False, abc=True)
