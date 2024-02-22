# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/14 21:39
"""
import os
import sys
p = "W:/projects/nzt/misc/users/yangtao/main_code"
p in sys.path or sys.path.append(p)

from missions import MissionsPlanner

import project_files


def build_mission():
    output_dir = "W:/projects/nzt/misc/users/yangtao/output/files_collection/comp_mission"
    mission_path = output_dir + "/mission"

    mp = MissionsPlanner(mission_path)
    for file in project_files.get_w_max_files("bil", "n10", ["ani", "lay"]):
        mp.create_missions(mission_name=os.path.basename(file),
                           python_script=__file__,
                           fun_name="run_mission",
                           fun_args=[file,
                                     output_dir]
                           )


def run_mission(maya_file, output_dir):
    # 'W:/projects/bil/shot/n10/n10050/ani/maya/n10050.ani.animation.v003.ma'

    print("maya_file: ", maya_file)
    print("output_dir: ", output_dir)

    import maya.cmds as cmds
    import sys

    p = "W:/projects/nzt/misc/users/yangtao/main_code"
    p in sys.path or sys.path.append(p)

    from playblast import pb_main

    cmds.file(maya_file,
              open=True,
              prompt=False,
              ignoreVersion=True,
              f=True)

    cmds.currentUnit(t="30fps")

    shot_name = os.path.basename(maya_file).split(".")[0]
    sg_cut_in, sg_cut_out = project_files.get_shot_frames("bil", shot_name)
    cmds.playbackOptions(min=int(sg_cut_in), max=int(sg_cut_out))

    if cmds.objExists("ruins_env:Root_grp"):
        cmds.setAttr("ruins_env:Root_grp.visibility", 0)

    if not cmds.objExists("ruins_asb_AR"):
        ruins_asb = "I:/projects/bil/asset/asb/ruins_asb/mod/ruins_asb.mod.model/assembly_definition/ruins_asb.ma"
        asb_node = cmds.container(type='assemblyReference', name='ruins_asb_AR')
        cmds.setAttr(asb_node + '.def', ruins_asb, type='string')
        cmds.namespace(rename=(cmds.assembly(asb_node, q=1, repNamespace=1), asb_node + '_ASB'))

    mov_file = output_dir + "/" + os.path.splitext(os.path.basename(maya_file))[0] + ".mov"
    pb_main.run(mov_file, width=2048, height=1152)


if __name__ == '__main__':
    build_mission()
