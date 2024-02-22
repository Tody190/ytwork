# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/10/27 15:13
"""
import json
import os
import pprint

from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path


ani_path = "I:/projects/fgt/shot/z90/z90060/lay/z90060.lay.rough_layout"
shot_name = os.path.basename(ani_path).split(".")[0]
asset_name = shot_name + "_BG"
asset_cmp_json = "I:/projects/fgt/asset/asb/%s/mod/%s.mod.model/asset_components.json" % (asset_name, asset_name)

with open(asset_cmp_json, "r") as asset_cmp_f:
    asset_cmp_data = json.load(asset_cmp_f)

shot_cmp_file = ani_path + "/shot_components.json"
with open(shot_cmp_file, "r") as shot_cmp_f:
    shot_cmp_data = json.load(shot_cmp_f)
    for shot_cmp_name in shot_cmp_data:
        # z90070_BG:stone_xy_a13_AR
        # stone_xy_a13_AR
        asset_cmp_name = shot_cmp_name.split(":")[-1]
        if asset_cmp_name in asset_cmp_data:
            shot_cmp_data[shot_cmp_name]["look_pass"] = asset_cmp_data[asset_cmp_name]["look_pass"]

    pprint.pprint(shot_cmp_data)

unlock_path(ani_path)
unlock_path(shot_cmp_file)

with open(shot_cmp_file, "w") as new_shot_cmp_f:
    json.dump(shot_cmp_data, new_shot_cmp_f, indent=4, ensure_ascii=False, sort_keys=True)

lock_path(shot_cmp_file)
lock_path(ani_path)