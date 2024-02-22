# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/18 22:09
"""
import os.path

import maya.cmds as mc
import sys
import json
import glob

p = "W:/projects/nzt/misc/users/yangtao/main_code"
p in sys.path or sys.path.append(p)
from playblast import pb_main
import project_files

from missions import MissionsPlanner


def build_mission():
    output_dir = "W:/projects/bil/misc/users/yangtao/scn_pb"
    mp = MissionsPlanner(output_dir + "/mission")

    scn_task_paths = glob.glob("I:/projects/bil/shot/*/*/scn")
    for task_p in scn_task_paths:
        task_p = task_p.replace("\\", "/")
        shot_name = task_p.split("/")[-2]
        ver_d_name_list = glob.glob(task_p + "/" + shot_name + ".scn.scene.*")
        if ver_d_name_list:
            max_ver_d_name = sorted(ver_d_name_list, reverse=True)[0]
            shot_components = max_ver_d_name.replace("\\", "/") + "/shot_components.json"

            if not os.path.exists(shot_components):
                print("No shot_components", shot_name)
                continue

            i_p = "I:/projects/bil/shot/{seq}/{shot}/ani/".format(seq=shot_name[:3], shot=shot_name)
            i_p += "{shot}.ani.animation/{shot}.ani.animation.*.ma".format(shot=shot_name)

            w_ani_p = "W:/projects/bil/shot/{seq}/{shot}/ani/maya/".format(seq=shot_name[:3], shot=shot_name)
            w_ani_p += "{shot}.ani.animation.*.ma".format(shot=shot_name)

            w_lay_p = "W:/projects/bil/shot/{seq}/{shot}/lay/maya/".format(seq=shot_name[:3], shot=shot_name)
            w_lay_p += "{shot}.lay.rough_layout.*.ma".format(shot=shot_name)

            max_ani_ver_f = None
            for p_pattern in (i_p, w_ani_p, w_lay_p):
                f_list = glob.glob(p_pattern)
                if f_list:
                    max_ani_ver_f = sorted(f_list, reverse=True)[0]
                    if max_ani_ver_f and os.path.isfile(max_ani_ver_f):
                        max_ani_ver_f = max_ani_ver_f.replace("\\", "/")
                        print(max_ani_ver_f)
                        break

            if max_ani_ver_f:
                # if not os.path.exists(mov_file):
                mp.create_missions(mission_name=os.path.basename(max_ani_ver_f),
                                   python_script=__file__,
                                   fun_name="run_mission",
                                   fun_kwargs={"ani_maya_file": max_ani_ver_f,
                                               "scn_comp_json": shot_components,
                                               "output_dir": output_dir}
                                   )


def organize_outline():
    ignore_nodes = ["|cam", "|asset"]
    for top_node in mc.ls(assemblies=True, l=True):
        if top_node not in ignore_nodes:
            try:
                mc.setAttr(top_node + ".visibility", 0)
            except:
                pass

    if mc.objExists("|asset"):
        for obj in mc.listRelatives("|asset", c=True, fullPath=True):
            try:
                mc.setAttr(obj + ".visibility", 1)
            except:
                pass


asb_asset_map = {"ruins_asb":
                     "I:/projects/bil/asset/asb/ruins_asb/mod/ruins_asb.mod.model/assembly_definition/ruins_asb.ma"}


def reload_asb(asb_info):
    if not mc.objExists("|asset|asb"):
        mc.group(name="asb", em=1, p="|asset")

    if mc.objExists(asb_info["component_node"]):
        for obj in mc.ls(asb_info["component_node"], l=True):
            mc.delete(obj)

    asb_node = mc.container(type='assemblyReference', name=asb_info["component_node"])
    mc.setAttr(asb_node + '.def', asb_asset_map[asb_info["asset_name"]], type='string')
    mc.namespace(rename=(mc.assembly(asb_node, q=1, repNamespace=1), asb_info["namespace"]))

    mc.parent(asb_node, "|asset|asb")


def run_mission(ani_maya_file, scn_comp_json, output_dir):
    print("maya_file: ", ani_maya_file)
    print("scn_comp_file: ", scn_comp_json)
    print("output_dir: ", ani_maya_file)

    error_log_f = output_dir.replace("\\", "/") + "/" + os.path.basename(ani_maya_file) + ".log"

    mc.file(ani_maya_file, open=True, prompt=False, ignoreVersion=True, f=True)

    mc.currentUnit(t="30fps")

    shot_name = os.path.basename(ani_maya_file).split(".")[0]
    sg_cut_in, sg_cut_out = project_files.get_shot_frames("bil", shot_name)
    mc.playbackOptions(min=int(sg_cut_in), max=int(sg_cut_out))

    organize_outline()

    with open(scn_comp_json, 'r') as f:
        scn_comp_data = json.load(f)

    asb_info = {}
    for comp_name, comp_data in scn_comp_data.items():
        is_root = comp_data.get("is_root", False)
        if comp_data.get("type", "") == "assembly" and is_root:
            asb_info["asset_name"] = comp_data.get("asset_name", "")
            asb_info["component_node"] = comp_data.get("component_node", "")
            asb_info["namespace"] = comp_data.get("namespace", "")
    if asb_info:
        reload_asb(asb_info)

    error_log_info = ""
    for comp_name, comp_data in scn_comp_data.items():
        dag_path = comp_data.get("dag_path")
        if dag_path:
            object_xform = comp_data.get("transform_hi", "")
            if object_xform:
                if mc.objExists(dag_path):
                    if object_xform:
                        mc.xform(dag_path, ws=1, m=eval(object_xform))
                        print(dag_path.split("|")[-1], object_xform)
                else:
                    e_info = "No DAG path: " + dag_path + "\n"
                    print(e_info)
                    error_log_info += e_info

    if error_log_info:
        head = "ani file: %s\n" % ani_maya_file
        head += "scn comp json: %s\n\n" % scn_comp_json

        error_log_info = head + error_log_info

        with open(error_log_f, 'w') as f:
            f.write(error_log_info)

    mov_file = output_dir + "/" + os.path.splitext(os.path.basename(ani_maya_file))[0] + ".mov"
    pb_main.run(mov_file, width=2048, height=1152)


if __name__ == '__main__':
    build_mission()
