# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/21 16:19
"""

import glob
import os
import pprint
import sys

import maya.cmds as mc

from oct.pipeline.path import unlock_path

p = "W:/projects/nzt/misc/users/yangtao/main_code"
p in sys.path or sys.path.append(p)
from playblast import pb_main
from batch_repair import my_maya_util
import project_files
from missions import MissionsPlanner


def unload_reference(ignore_objects_parent):
    # 获取需要保留的资产
    ignore_objects_rfn = []
    for need_retained_parent in ignore_objects_parent:
        if mc.objExists(need_retained_parent):
            rel = mc.listRelatives(need_retained_parent, c=True, fullPath=True)
            if rel:
                for obj in rel:
                    if mc.referenceQuery(obj, isNodeReferenced=True):
                        ignore_objects_rfn.append(mc.referenceQuery(obj, rfn=True))

    for rfn in mc.ls(references=True):
        if rfn not in ignore_objects_rfn:
            try:
                reference_path = mc.referenceQuery(rfn, filename=True)
                mc.file(reference_path, removeReference=True, f=True)
            except Exception as e:
                print(e)


def recursive_delete(node):
    for node in mc.ls(node, l=True):
        children = mc.listRelatives(node, children=True)
        if children:
            for child in children:
                recursive_delete(child)

        if mc.objExists(node):
            try:
                mc.lockNode(node, lock=False)
                mc.delete(node)
            except Exception as e:
                print(e)


def del_top_object(ignore_objects):
    _ignore_list = ["|persp", "|top", "|front", "|side", "|left"]
    ignore_objects += _ignore_list + ignore_objects

    for top in mc.ls(assemblies=True, l=True):
        if top not in ignore_objects:
            recursive_delete(top)


def vis_top_object(ignore_objects, vis=True):
    _ignore_list = ["|persp", "|top", "|front", "|side", "|left"]
    ignore_objects += _ignore_list + ignore_objects

    for top in mc.ls(assemblies=True, l=True):
        if top not in ignore_objects:
            try:
                mc.setAttr(top + ".visibility", vis)
            except Exception as e:
                print(e)


def organize_scn_env():
    retained_objs = ["|asset|env", "|asset|asb", "|asset|flg"]
    # 将需要的部分移动到 retained_grp
    if not mc.objExists("retained_grp"):
        mc.group(empty=True, name="retained_grp")
    for obj in retained_objs:
        if mc.objExists(obj):
            mc.parent(obj, "retained_grp")

    # 移除不需要的引用
    unload_reference(ignore_objects_parent=["|retained_grp|env",
                                            "|retained_grp|asb",
                                            "|retained_grp|flg"])
    # 删除不需要的顶级节点
    del_top_object(ignore_objects=["|retained_grp"])

    # 删除显示层
    my_maya_util.del_all_display_layers()

    # 删除动画层
    my_maya_util.remove_all_animation_layers()

    # 清除命名空间
    my_maya_util.remove_unused_namespaces()


def ani_import_env(env_ma_path):
    """
    # 移除 ani 场景
    :param env_ma_path:
    :return:
    """

    # 移除不需要的引用
    unload_reference(ignore_objects_parent=["|asset|chr",
                                            "|asset|prp",
                                            "|cam",
                                            "cam_rig_grp"])

    # 删除不需要部分
    for obj in ["|asset|flg", "|asset|env", "|asset|asb"]:
        if mc.objExists(obj):
            recursive_delete(obj)

    # 隐藏不需要的顶级节点
    vis_top_object(ignore_objects=["|asset", "|cam"], vis=False)

    # 导入 env 资产
    mc.file(env_ma_path,
            i=True,
            ignoreVersion=True,
            namespace=":",
            pr=True)

    # 整理组
    for grp_name in ["env", "asb", "flg"]:
        retained_grp_name = "|retained_grp|" + grp_name
        if mc.objExists(retained_grp_name):
            rel = mc.listRelatives(retained_grp_name, c=True, fullPath=True)
            if rel:
                for o in rel:
                    asset_path = "|asset|" + grp_name
                    if not os.path.exists(asset_path):
                        mc.group(empty=True, parent="asset", name=grp_name)

                    mc.parent(o, asset_path)

    # recursive_delete("|retained_grp")


def get_files():
    scn_and_ani_files = []

    scn_task_paths = glob.glob("I:/projects/bil/shot/*/*/scn")
    for task_p in scn_task_paths:
        task_p = task_p.replace("\\", "/")
        shot_name = task_p.split("/")[-2]
        ver_d_name_list = glob.glob(task_p + "/" + shot_name + ".scn.scene.*")
        if ver_d_name_list:
            max_ver_d_name = sorted(ver_d_name_list, reverse=True)[0]
            scn_ma_files = glob.glob(max_ver_d_name.replace("\\", "/") + "/*.ma")
            if scn_ma_files:
                scn_ma = scn_ma_files[0].replace("\\", "/")

                shot_name = scn_ma.split("/")[5]
                seq_name = shot_name[:3]

                ani_temp = "I:/projects/bil/shot/{seq}/{shot}/ani/{shot}.ani.animation/{shot}.ani.animation.*.ma"
                ani_ma_glob = ani_temp.format(seq=seq_name, shot=shot_name)
                ani_ma_files = glob.glob(ani_ma_glob)
                if ani_ma_files:
                    ani_ma = ani_ma_files[0].replace("\\", "/")
                    scn_and_ani_files.append((scn_ma, ani_ma))

    return scn_and_ani_files


def rename_asb_ns():
    # if not mc.objExists("|asset|asb"):
    #     return
    #
    # asb_node = mc.listRelatives("|asset|asb", c=True, fullPath=True,)
    # if not asb_node:
    #     return

    asb_node = mc.ls(type="assemblyReference", l=True)

    for n in asb_node:
        ns = mc.getAttr(n + ".repNamespace")
        if ns.endswith("_AR_ASB"):
            try:
                mc.setAttr(n + ".repNamespace", ns.replace("_AR_ASB", ""), type="string")
            except Exception as e:
                print(e)


def run_mission(scn_ma, ani_ma, output_dir, playblast=False):
    mc.currentUnit(t="30fps")

    # 打开文件 scn 文件
    mc.file(scn_ma,
            open=True,
            prompt=False,
            ignoreVersion=True,
            f=True)

    # 整理置景文件
    organize_scn_env()

    # 将文件保存到temp
    scene_path = os.path.dirname(scn_ma)
    unlock_path(scene_path)
    temp_path = scene_path + "/temp"
    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)
    env_ma = temp_path + "/env.ma"

    mc.file(rename=env_ma)
    mc.file(save=True)

    # 打开动画文件
    mc.file(ani_ma,
            open=True,
            prompt=False,
            ignoreVersion=True,
            f=True)

    # 整理并导入置景文件
    ani_import_env(env_ma)

    rename_asb_ns()

    # 清除命名空间
    my_maya_util.remove_unused_namespaces()

    # 另存
    savs_as_file = output_dir + "/" + os.path.basename(ani_ma)
    mc.file(rename=savs_as_file)
    mc.file(save=True)

    if playblast:
        mov_file = output_dir + "/" + os.path.splitext(os.path.basename(ani_ma))[0] + ".mov"
        # 拍屏
        shot_name = os.path.basename(ani_ma).split(".")[0]
        sg_cut_in, sg_cut_out = project_files.get_shot_frames("bil", shot_name)
        mc.playbackOptions(min=int(sg_cut_in), max=int(sg_cut_out))

        pb_main.run(mov_file, width=2048, height=1152)


def build_mission():
    output_dir = "W:/projects/bil/misc/users/yangtao/scn_pb"
    mission_path = output_dir + "/mission"

    mp = MissionsPlanner(mission_path)

    for scn_ma, ani_ma in get_files():
        mp.create_missions(mission_name=os.path.basename(ani_ma),
                           python_script=__file__,
                           fun_name="run_mission",
                           fun_kwargs={"scn_ma": scn_ma,
                                       "ani_ma": ani_ma,
                                       "output_dir": output_dir}
                           )


if __name__ == '__main__':
    build_mission()