# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/25 18:55
"""
import glob
import os
import shutil

import project_files

src_p = "W:/projects/nzt/misc/users/yangtao/output/i20"

for preview_f in glob.glob(src_p + "/*.mov"):
    #oct_shot = os.path.basename(preview_f).split(".")[0]
    kekedou_preview_name = project_files.get_kekedou_version_name(os.path.basename(preview_f))

    dst_p = src_p + "/kkd_preview"
    kekedou_preview_name_f = os.path.join(dst_p, kekedou_preview_name)

    shutil.copy(preview_f, kekedou_preview_name_f)
