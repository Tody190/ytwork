# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/9 21:12
"""
import os

import maya.cmds as cmds

from oct_maya.tools.ani.oct_playblast_tool import app_launcher


class PbTool(object):
    def __init__(self):
        cameras = cmds.ls('??????_cam')
        if cameras:
            self.cam = cameras[0]
        else:
            return

    def set_modeEditor(self):
        cmds.lookThru(self.cam)
        activeEditor = cmds.playblast(ae=1)
        cmds.modelEditor(activeEditor, e=1, av=1, cam=self.cam,
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
                         cameras=False)

    def set_scence(self):
        for nemo_n in cmds.ls('*:*', type='Nemo'):
            cmds.setAttr(nemo_n + '.write', True)

        self.set_modeEditor()

    def paly(self, output_file):
        try:
            self.set_scence()
        except Exception as e:
            print(e)

        ol = app_launcher.OctLauncher()
        ol.output_path = output_file
        ol.view_result = False
        ol.auto_audio_update = True

        ol.execute_cmd()


def run(output_file):
    pbt = PbTool()
    pbt.paly(output_file)