# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/11 22:22
"""
import os

import project_files
import glob


mov_files_path = "W:/projects/nzt/misc/users/yangtao/i10_s075001"

mov_files = glob.glob(mov_files_path + "/*.mov")

for m_f in mov_files:
    oct_version_name = os.path.basename(m_f)
    kkd_shot_name = project_files.get_kekedou_version_name(oct_version_name)
    rename_f = os.path.dirname(m_f) + "/rename/%s.mov" % kkd_shot_name
    print(rename_f)
    os.rename(m_f, rename_f)