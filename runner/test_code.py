# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/11 9:39
"""


# from oct.pipeline.path import unlock_path
#
# p = "I:/projects/fgt/shot/z90/z90080/lay/z90080.lay.rough_layout.v001"
# unlock_path(p, recursive=True)

# comp_cache_data = {u'ruins_asb.bush_l2_AR': [u'I:/projects/bil/cache/n10/n10020/ruins_asb.bush_l2_AR/n10020.ani.animation.v009/ruins_asb.bush_l2_AR.abc', u'I:/projects/bil/cache/n10/n10020/ruins_asb.bush_l2_AR/n10020.ani.animation.v009/ruins_asb.bush_l2_AR.v001.abc'], u'ruins_asb.bush_a3_AR': [u'I:/projects/bil/cache/n10/n10020/ruins_asb.bush_a3_AR/n10020.ani.animation.v009/ruins_asb.bush_a3_AR.abc', u'I:/projects/bil/cache/n10/n10020/ruins_asb.bush_a3_AR/n10020.ani.animation.v009/ruins_asb.bush_a3_AR.v001.abc'], 'cam': ['I:/projects/bil/cache/n10/n10020/cam/n10020.ani.animation.v009/cam.usd', 'I:/projects/bil/cache/n10/n10020/cam/n10020.ani.animation.v009/cam.v012.usd'], u'ruins_asb.bush_m1_AR': [u'I:/projects/bil/cache/n10/n10020/ruins_asb.bush_m1_AR/n10020.ani.animation.v009/ruins_asb.bush_m1_AR.abc', u'I:/projects/bil/cache/n10/n10020/ruins_asb.bush_m1_AR/n10020.ani.animation.v009/ruins_asb.bush_m1_AR.v001.abc']}
# version_name = 'n10020.ani.animation.v009'
# shot_code = 'n10020'
# proj = 'bil'
#
# from toolsets.tools.flo.usd_creation import cache_usd_creator
#
# for comp in comp_cache_data.keys():
#     if comp == "cam":
#         # ruins_asb.bush_m2_AR
#         creator = cache_usd_creator.AnimatedCacheUsdCreator(comp, version_name, shot_code, proj)
#         creator.update_cache_usd()

import glob
import os
from oct.pipeline.path import symlink

# link_p_1 = "I:/projects/bil/cache/n10/n10020/cam/n10020.ani.animation.v009/cam.v015.usd"
# link_p_2 = "I:/projects/bil/cache/n10/n10020/cam/n10020.ani.animation.v009/cam.usd"


# link_p_1 = "I:/projects/bil/cache/n10/n10020/cam/n10020.ani.animation.v009/cam.v015.abc"
# link_p_2 = "I:/projects/bil/cache/n10/n10020/cam/n10020.ani.animation.v009/cam.abc"

# if os.path.exists(link_p_2):
#     os.remove(link_p_2)
# symlink(link_p_1, link_p_2, exist_remove=True)


# from oct.pipeline.path import unlock_path
# from oct.pipeline.path import lock_path
#
# import maya.cmds as mc
#
# cam_cache_glob = "I:/projects/bil/cache/*/*/cam"
#
# for cam_d in glob.glob(cam_cache_glob):
#     cam_version_dir_list = []
#     for cam_version_dir in os.listdir(cam_d):
#         if ".ani.animation." in cam_version_dir:
#             cam_version_dir_list.append(cam_version_dir)
#
#     cam_version_dir_list = sorted(cam_version_dir_list)
#     max_version_dir = cam_version_dir_list[-1]
#
#     cam_abc_file = os.path.join(cam_d, max_version_dir, "cam.abc")
#     cam_abc_file = cam_abc_file.replace("\\", "/")
#     if os.path.exists(cam_abc_file):
#
#     break

from oct.pipeline.path import symlink
v000 = "I:/projects/fgt/asset/prp/z090_shu/rig/z090_shu.rig.rigging.v000"
symlink(v000,
        "I:/projects/fgt/asset/prp/z090_shu/rig/z090_shu.rig.rigging", exist_remove=True)
