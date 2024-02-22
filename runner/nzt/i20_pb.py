# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/22 17:26
"""
import glob
import json
import os.path

import maya.cmds as mc

import project_files
reload(project_files)
import batch_repair.my_maya_util as maya_util
reload(maya_util)
from playblast import pb_main
reload(pb_main)
from missions import MissionsPlanner


replace_map = {"MiLin_ShangY":
                   "I:/projects/nzt/asset/asb/s076001woods/mod/s076001woods.mod.model/s076001woods.ma"}

assets_file_map = {
    "s075001deeppool": "I:/projects/nzt/asset/asb/s075001deeppool/mod/s075001deeppool.mod.model/s075001deeppool.ma",
    "s076001woods": "I:/projects/nzt/asset/asb/s076001woods/mod/s076001woods.mod.model/s076001woods.ma"}

shot_asset_map = {'i20010': ['s075001deeppool'],
                  'i20020': ['s075001deeppool'],
                  'i20030': ['s075001deeppool'],
                  'i20040': ['s075001deeppool'],
                  'i20050': ['s075001deeppool'],
                  'i20070': ['s076001woods'],
                  'i20080': ['s076001woods'],
                  'i20090': ['s075001deeppool'],
                  'i20100': ['s075001deeppool'],
                  'i20110': ['s075001deeppool'],
                  'i20120': ['s075001deeppool'],
                  'i20130': ['s076001woods'],
                  'i20170': ['s076001woods'],
                  'i20180': ['s075001deeppool'],
                  'i20190': ['s075001deeppool'],
                  'i20200': ['s075001deeppool'],
                  'i20210': ['s075001deeppool'],
                  'i20220': ['s075001deeppool'],
                  'i20230': ['s075001deeppool'],
                  'i20240': ['s075001deeppool'],
                  'i20250': ['s075001deeppool'],
                  'i20260': ['s075001deeppool'],
                  'i20270': ['s075001deeppool'],
                  'i20280': ['s075001deeppool'],
                  'i20290': ['s075001deeppool'],
                  'i20300': ['s075001deeppool'],
                  'i20310': ['s075001deeppool', 's076001woods'],
                  'i20320': ['s075001deeppool'],
                  'i20330': ['s076001woods'],
                  'i20340': ['s076001woods'],
                  'i20350': ['s075001deeppool'],
                  'i20360': ['s076001woods'],
                  'i20370': ['s075001deeppool', 's076001woods'],
                  'i20380': ['s075001deeppool'],
                  'i20390': ['s076001woods'],
                  'i20400': ['s076001woods'],
                  'i20410': ['s076001woods'],
                  'i20420': ['s076001woods'],
                  'i20430': ['s075001deeppool', 's076001woods'],
                  'i20440': ['s076001woods'],
                  'i20450': ['s076001woods'],
                  'i20460': ['s075001deeppool', 's076001woods'],
                  'i20470': ['s076001woods'],
                  'i20480': ['s076001woods'],
                  'i20490': ['s075001deeppool', 's076001woods'],
                  'i20500': ['s075001deeppool'],
                  'i20510': ['s076001woods'],
                  'i20520': ['s076001woods'],
                  'i20530': ['s076001woods'],
                  'i20540': ['s075001deeppool', 's076001woods'],
                  'i20550': ['s076001woods'],
                  'i20560': ['s076001woods'],
                  'i20570': ['s076001woods'],
                  'i20580': ['s076001woods'],
                  'i20600': ['s075001deeppool'],
                  'i20610': ['s075001deeppool', 's076001woods'],
                  'i20620': ['s075001deeppool', 's076001woods'],
                  'i20630': ['s076001woods'],
                  'i20640': ['s075001deeppool', 's076001woods'],
                  'i20650': ['s076001woods'],
                  'i20660': ['s075001deeppool', 's076001woods'],
                  'i20670': ['s076001woods'],
                  'i20680': ['s076001woods'],
                  'i20690': ['s075001deeppool'],
                  'i20700': ['s076001woods'],
                  'i20710': ['s075001deeppool'],
                  'i20720': ['s076001woods'],
                  'i20730': ['s076001woods'],
                  'i20740': ['s075001deeppool', 's076001woods'],
                  'i20750': ['s076001woods'],
                  'i20760': ['s075001deeppool'],
                  'i20770': ['s076001woods'],
                  'i20780': ['s076001woods'],
                  'i20790': ['s075001deeppool', 's076001woods'],
                  'i20800': ['s075001deeppool'],
                  'i20810': ['s075001deeppool', 's076001woods'],
                  'i20820': ['s076001woods'],
                  'i20840': ['s075001deeppool', 's076001woods'],
                  'i20850': ['s075001deeppool', 's076001woods']
                  }


def build_mission():
    output_dir = "W:/projects/nzt/misc/users/yangtao/output/i20"
    mission_path = output_dir + "/mission"

    mp = MissionsPlanner(mission_path)
    for shot_name in shot_asset_map.keys():
        mp.create_missions(mission_name=os.path.basename(shot_name),
                           python_script=__file__,
                           fun_name="run_mission",
                           fun_args=[shot_name,
                                     output_dir]
                           )

def build_mission_new():
    output_dir = "W:/projects/nzt/misc/users/yangtao/output/i20"
    mission_path = output_dir + "/mission"

    mp = MissionsPlanner(mission_path)
    for ma_file in glob.glob(output_dir + "/*.ma"):
        ma_file = ma_file.replace("\\", "/")
        mp.create_missions(mission_name=os.path.basename(ma_file),
                           python_script=__file__,
                           fun_name="playblast_mission",
                           fun_args=[ma_file,
                                     output_dir]
                           )


def get_all_reference_assets():
    # 找到场景内所有 reference 资产名
    reference_scenes = []
    for rfn in mc.ls(type="reference"):
        if "RN" in str(rfn):
            reference_scenes.append(str(rfn).split("RN")[0])

    return reference_scenes


def playblast_mission(maya_file, output_dir):
    print("maya_file: ", maya_file)
    print("output_dir: ", output_dir)

    mov_file = output_dir + "/" + os.path.splitext(os.path.basename(maya_file))[0] + ".mov"
    print("mov_file: ", mov_file)

    mc.file(maya_file, open=True, f=True)
    # 隐藏所有参考
    pb_main.organize_outline()
    # 适配帧范围
    shot_name = os.path.basename(maya_file).split(".")[0]
    pb_main.fit_frame_range("nzt", shot_name)
    pb_main.run(mov_file, width=2048, height=1080)


def run_mission(shot_name, output_dir):
    pub_files = project_files.get_projcet_files("nzt", "ani.animation", shot_start_with=shot_name)
    if not pub_files:
        pub_files = project_files.get_projcet_files("nzt", "lay.rough_layout", shot_start_with=shot_name)

    pub_file = pub_files[0]

    file_no_ext_name = os.path.splitext(os.path.basename(pub_file))[0]

    log_json_data = {"orig_scenes_rfn": {},
                     "replace_scenes_rfn": {}}
    log_json_f = os.path.join(output_dir, file_no_ext_name + ".json")

    mc.file(pub_file, open=True, prompt=False, ignoreVersion=True, f=True)

    # 获取原始场景资产引用信息
    for rfn in mc.ls(type="reference"):
        try:
            ref_file_path = mc.referenceQuery(rfn, filename=True)
            log_json_data["orig_scenes_rfn"][rfn] = ref_file_path
        except Exception as e:
            print(e)

    maya_util.remove_unused_namespaces()
    maya_util.clean_scene()

    need_ref_assets = shot_asset_map.get(shot_name, [])
    # 替换引用
    for rfn_asset in get_all_reference_assets():
        if rfn_asset in replace_map.keys():
            maya_util.replace_reference(ref=rfn_asset + "RN",
                                        new_ref=replace_map[rfn_asset])

        # 移除引用, 是 05 或 06， 但是不应该在场景里
        if rfn_asset in assets_file_map.keys() and rfn_asset not in need_ref_assets:
            reference_path = mc.referenceQuery(rfn_asset + "RN", filename=True)
            mc.file(reference_path, removeReference=True, f=True)
            print("------------" + rfn_asset + "RN" + " removed")

    maya_util.remove_unused_namespaces()
    maya_util.clean_scene()

    # 应该存在的场景
    for correct_asset in shot_asset_map.get(shot_name, []):
        if correct_asset not in get_all_reference_assets():
            print("correct_asset: ", correct_asset)
            reference_f = assets_file_map.get(correct_asset, "")
            if reference_f:
                mc.file(assets_file_map[correct_asset], reference=True, namespace=correct_asset)

                ns = mc.referenceQuery(reference_f, namespace=True)
                root_grp = ns + ":Root_grp"
                if mc.objExists(root_grp):
                    try:
                        mc.parent(root_grp, "|asset|asb")
                    except Exception as e:
                        print(e)

    maya_util.remove_unused_namespaces()
    maya_util.clean_scene()

    new_file = os.path.join(output_dir, os.path.basename(pub_file)).replace("\\", "/")
    mc.file(rename=new_file)
    mc.file(save=True)

    # 获取原始场景资产引用信息
    for rfn in mc.ls(type="reference"):
        try:
            ref_file_path = mc.referenceQuery(rfn, filename=True)
            log_json_data["replace_scenes_rfn"][rfn] = ref_file_path
        except Exception as e:
            print(e)

    with open(log_json_f, "w") as f:
        json.dump(log_json_data, f, indent=4, sort_keys=True)

    sg_cut_in, sg_cut_out = project_files.get_shot_frames("nzt", shot_name)
    mc.playbackOptions(min=int(sg_cut_in), max=int(sg_cut_out))

    mov_file = output_dir + "/" + os.path.splitext(os.path.basename(pub_file))[0] + ".mov"
    print("mov_file: ", mov_file)
    pb_main.run(mov_file, width=2048, height=1080)


if __name__ == '__main__':
    build_mission_new()