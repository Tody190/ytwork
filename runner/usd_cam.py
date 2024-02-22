# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/30 19:29
"""

import glob
import os
import pprint

import project_files
try:
    import maya.cmds as mc
except:
    pass

from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path





def run(cam_cache_glob, write_usda=True):
    for cam_d in glob.glob(cam_cache_glob):
        print(cam_d)
        cam_version_dir_list = []
        for cam_version_dir in os.listdir(cam_d):
            if ".ani.animation." in cam_version_dir:
                cam_version_dir_list.append(cam_version_dir)
        if not cam_version_dir_list:
            for cam_version_dir in os.listdir(cam_d):
                if ".ani.blocking" in cam_version_dir:
                    cam_version_dir_list.append(cam_version_dir)
        if not cam_version_dir_list:
            for cam_version_dir in os.listdir(cam_d):
                if ".lay.rough_layout" in cam_version_dir:
                    cam_version_dir_list.append(cam_version_dir)

        cam_version_dir_list = sorted(cam_version_dir_list)
        max_version_dir = cam_version_dir_list[-1]

        cam_abc_file = os.path.join(cam_d, max_version_dir, "cam.abc")
        cam_abc_file = cam_abc_file.replace("\\", "/")
        if os.path.exists(cam_abc_file):
            proj = cam_abc_file.split("/")[2]
            seq = cam_abc_file.split("/")[4]
            shot = cam_abc_file.split("/")[5]
            cam_name = shot + "_cam"

            print(proj, seq, shot)

            mc.file(new=True, f=True)

            plugs = ["mayaUsdPlugin.mll"]
            for p in plugs:
                if not mc.pluginInfo(p, q=1, loaded=True):
                    mc.loadPlugin(p, quiet=True)

            mc.file(cam_abc_file, type='Alembic', i=True, mnc=True,
                    namespace=":", gl=True, ignoreVersion=True)

            if proj == "bil":
                mc.currentUnit(t="30fps")
            else:
                mc.currentUnit(t="24fps")

            start_time, end_time = project_files.get_shot_frames(proj, shot)
            start_time = start_time - 3
            end_time = end_time + 3
            print(start_time, end_time)
            mc.playbackOptions(min=int(start_time), max=int(end_time))

            sel_obj = mc.ls(cam_name, long=True)[0]
            mc.select(clear=True)
            mc.select(sel_obj)

            export_options = ";exportUVs=0;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportColorSets=0;"
            export_options += "defaultMeshScheme=catmullClark;defaultUSDFormat=usda;"
            export_options += "animation=1;eulerFilter=0;staticSingleSample=0;"
            export_options += "startTime={start};endTime={end};frameStride={step};frameSample=0.0;".format(
                                                                                                    start=start_time,
                                                                                                    end=end_time,
                                                                                                    step=0.2)
            export_options += "parentScope=;exportDisplayColor=0;shadingMode=none;exportInstances=1;"
            export_options += "exportVisibility=1;mergeTransformAndShape=0;stripNamespaces=0"
            export_options += "exportRoots={cam_root}".format(cam_root=sel_obj)

            usd_file = os.path.join(cam_d, max_version_dir, "cam")
            print("Options: ", export_options)
            print(usd_file)
            mc.file(usd_file, options=export_options, typ="USD Export", pr=True, es=True, f=True)

            if write_usda:
                usda_file = os.path.join(cam_d, "cam.usda")
                if os.path.exists(usda_file):
                    unlock_path(cam_d)

                    print("write usda file")
                    with open(usda_file, "r") as f:
                        usda_content = f.read()

                    with open(usda_file, "w") as f:
                        orig_cam = max_version_dir + "/cam.abc"
                        dst_cam = max_version_dir + "/cam.usd"
                        print(orig_cam, dst_cam)
                        usda_content = usda_content.replace(orig_cam, dst_cam)
                        f.write(usda_content)


def export_bil_usd_cam():
    cam_cache_glob = "I:/projects/bil/cache/*/*/cam"
    run(cam_cache_glob)


def export_nzt_usd_cam():
    cam_cache_glob = "I:/projects/nzt/cache/*/*/cam"
    run(cam_cache_glob, write_usda=False)


if __name__ == '__main__':
    for cam_d in glob.glob("I:/projects/bil/cache/n10/n10*/cam/cam.usda"):
        cam_d = cam_d.replace("\\", "/")
        shot_name = cam_d.split("/")[5]

        print("write usda file")
        with open(cam_d, "r") as f:
            usda_content = f.read()

        with open(cam_d, "w") as f:
            usda_content = usda_content.replace("/cam.usd", "/cam.abc")
            f.write(usda_content)


