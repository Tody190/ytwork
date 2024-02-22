# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/9 21:12
"""
import os

import maya.cmds as mc
import pymel.core as pm

import project_files


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

    image_planes = mc.ls(type='imagePlane')
    if image_planes:
        for i_p in image_planes:
            mc.setAttr(i_p + ".visibility", 0)


def fit_frame_range(projcet_name, shot_name):
    sg_cut_in, sg_cut_out = project_files.get_shot_frames(projcet_name, shot_name)
    mc.playbackOptions(min=int(sg_cut_in), max=int(sg_cut_out))

class PbTool(object):
    def __init__(self, **kwargs):
        cameras = mc.ls('??????_cam')
        if cameras:
            self.camera = cameras[0]
        else:
            return

        self.__data = {"fmt": "qt",
                       "qlt": 100,
                       "percent": 100,
                       "orn": False,
                       "v": False,
                       "fo": True,
                       "offScreen": True}

        if kwargs:
            self.__data.update(kwargs)

    def set_camera(self):
        mc.setAttr(self.camera + ".displayGateMaskOpacity", 1)
        mc.setAttr(self.camera + ".displayGateMaskColor", 0, 0, 0, type="double3")
        mc.camera(self.camera, e=True, dfg=True, dfo=False, dfp=False, dr=True, dsa=False, dst=False, dgm=True, overscan=1.0)
        mc.setAttr(self.camera + '.panZoomEnabled', False)
        mc.lookThru(self.camera)

    def set_modeEditor(self):
        activeEditor = mc.playblast(ae=1)
        mc.modelEditor(activeEditor, e=1, allObjects=True)
        mc.modelEditor(activeEditor, e=1, av=1, cam=self.camera,
                         displayLights="default",
                         displayAppearance='smoothShaded',
                         displayTextures=True,
                         motionTrails=False,
                         dimensions=False,
                         joints=False,
                         ikHandles=False,
                         handles=False,
                         follicles=False,
                         nRigids=False,
                         nurbsCurves=False,
                         locators=False,
                         sel=False,
                         grid=False,
                         pivots=False,
                         cameras=False,
                         xr=False)

    def set_scence(self):
        for nemo_n in mc.ls('*:*', type='Nemo'):
            mc.setAttr(nemo_n + '.write', True)

        try:
            # Wait for the cache loading
            gpu_cache_objects = mc.ls(type="gpuCache")
            if gpu_cache_objects:
                if not mc.pluginInfo('gpuCache', query=True, loaded=True):
                    mc.loadPlugin('gpuCache', f=True)

                mc.select(gpu_cache_objects, r=True)
                mc.gpuCache(query=True, waitForBackgroundReading=True)
                mc.select(cl=True)
        except Exception as e:
            print(e)

    def paly(self, output_file):
        self.set_scence()
        self.set_modeEditor()
        self.set_camera()

        mc.playblast(filename=output_file,
                       **self.__data)


def run(output_file, **kwargs):
    pbt = PbTool(**kwargs)
    pbt.paly(output_file)


def playblast_current_sence(output_dir):
    scene_name = mc.file(q=True, sceneName=True)
    print("maya_file: ", scene_name)
    projcet_name = scene_name.split("/")[2]
    shot_name = os.path.basename(scene_name).split(".")[0]
    print(projcet_name, shot_name)
    mov_file = output_dir + "/" + os.path.splitext(os.path.basename(scene_name))[0] + ".mov"
    print("output_move: ", mov_file)

    fit_frame_range(projcet_name, shot_name)
    organize_outline()

    print("mov_file: ", mov_file)
    run(mov_file, width=2048, height=1080)

