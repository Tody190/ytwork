# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/11/2 14:18
"""
import unreal


project_name = "fgt"
all_need_create_path = []

# Assets
# ------------------------------
assets_list = (
    ("chr", "xiaoming"),
    ("chr", "tianlangxing_didi"),
    ("chr", "ht_haita_a"),
    ("chr", "chali"),
    ("efx", "smoke"),)

asset_children = ["Blueprints", "Materials", "Models", "Rig", "Textures"]

for asset_type, asset_name in assets_list:
    for ac in asset_children:
        asset_p = "/game/{}/Assets/{}/{}/{}".format(project_name, asset_type, asset_name, ac)
        all_need_create_path.append(asset_p)

# Shots
# ------------------------------
level_shot = {"z90": ["z90010", "z90020", "z90030", "z90040", "z90050",
                      "z90060", "z90070", "z90080", "z90090"],
              "z91": ["z91020", "z91030", "z91040", "z91045", "z91046", "z91050",
                      "z91060", "z91070", "z91099"]}

level_children = ["animations", "Lighting", "Fx"]
for level_code, shot_code in level_shot.items():
    for shot in shot_code:
        for lc in level_children:
            level_path = "/game/{}/Sequences/{}/{}/{}".format(project_name, level_code, shot, lc)
            all_need_create_path.append(level_path)

# Others
# ------------------------------
other_paths = ["/game/Media/Audio/"]

for c_path in all_need_create_path:
    unreal.EditorAssetLibrary.make_directory(c_path)
