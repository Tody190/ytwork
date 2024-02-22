#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/22 14:22
# @Author  : YangTao

import os
import sys

import maya.standalone as standalone
standalone.initialize(name='python')
import pymel.core as pm
import maya.cmds as cmds

import pprint
import re
import importlib
import glob

add_sys_paths = ['D:/yangtao/pipeline_studio/packages/sutido_tools/maya_tools/1.0/python/maya_tools/tools/abctool',
                 'D:/yangtao/pipeline_studio/packages/sutido_tools/maya_tools/1.0/python/maya_tools/tools/hi_switcher']
for p in add_sys_paths:
    p in sys.path or sys.path.insert(0, p)

# cmds.loadPlugin(allPlugins=1)

import abcExport
# reload(abcExport)
import hi_main
# reload(hi_main)

cur_proj = 'AS24Y'


def export(export_wsd_file):
    cam_pattern = '.+_Cam'
    char_pattern = 'AS24Y_.+C.+_lo_.+|AS24Y_.+C.+_hi_.+'
    prop_pattern = 'AS24Y_.+P.+_lo_.+|AS24Y_.+P.+_hi_.+'
    set_pattern = '\\w+_S\\d+_\\w+_\\w+'

    cams = []
    chars = []
    props = []
    sets = []

    for fref in pm.listReferences(loaded=True):
        if re.match(char_pattern, str(fref.namespace)):
            chars.append(fref)
        if re.match(prop_pattern, str(fref.namespace)):
            props.append(fref)
        if re.match(set_pattern, str(fref.namespace)):
            sets.append(fref)

        for cam in pm.ls(cameras=True):
            if re.match(cam_pattern, cam.name()):
                cams.append(cam)

    export_abc = chars + props
    abcExport.export_scene(export_wsd_file, cur_proj, cams, export_abc, sets)


def get_ani_path_map():
    ani_files = []
    p = 'Z:/cgteamwork7/AS24Y_STUN/shot_work/animation/*/*/final'
    ani_final_path = glob.glob(p)
    for f in ani_final_path:
        mb_fils = []
        ani_files_name = os.listdir(f)
        if ani_files_name:
            for a_f in ani_files_name:
                if a_f.endswith('.mb'):
                    mb_fils.append(a_f)
            mb_fils = sorted(mb_fils)
            ani_f_name = mb_fils[-1]
            ani_file = os.path.join(f, ani_f_name).replace('\\', '/')
            ani_files.append(ani_file)

    return ani_files


def clean_scene():
    off_options = ['deformerOption', 'locatorOption', 'unusedNurbsSrfOption', 'nurbsCrvOption',
                   'expressionOption', 'poseOption', 'cachedOption', 'transformOption',
                   'partitionOption', 'kRemovingUnusedBrushes', 'ptConOption', 'unusedSkinInfsOption',
                   'setsOption']

    clean_options = ['nurbsSrfOption', 'displayLayerOption', 'renderLayerOption',
                     'animationCurveOption', 'groupIDnOption',
                     'shaderOption', 'shaderOption', 'ptConOption', 'pbOption', 'snapshotOption',
                     'unitConversionOption', 'referencedOption',
                     'brushOption', 'unknownNodesOption', 'clipOption']
    #
    # if hasattr(self.dialog, 'coco_v'):
    #     off_options.append('unusedSkinInfsOption')
    #     clean_options.remove('unusedSkinInfsOption')

    for option in off_options:
        cmds.optionVar(intValue=(option, False))

    for option in clean_options:
        cmds.optionVar(intValue=(option, True))

    os.environ['MAYA_TESTING_CLEANUP'] = '1'
    cmds.eval('source cleanUpScene.mel')
    cmds.eval('cleanUpScene(1)')
    os.environ['MAYA_TESTING_CLEANUP'] = ''

    for option in clean_options:
        cmds.optionVar(intValue=(option, False))

    if cmds.objExists('defaultLegacyAssetGlobals'):
        cmds.lockNode('defaultLegacyAssetGlobals', lock=False)
        cmds.delete('defaultLegacyAssetGlobals')


def start(export_path, *args):
    for ani_f in get_ani_path_map():
        try:
            shot_name = ani_f.split('/')[6]
            if shot_name not in args:
                continue

            print(shot_name, ": ", ani_f)

            if cmds.pluginInfo('mtoa', query=True, loaded=True):
                cmds.unloadPlugin('mtoa', force=True)

            cmds.file(ani_f, force=True, open=True, prompt=False)

            if cmds.pluginInfo('mtoa', query=True, loaded=True):
                cmds.unloadPlugin('mtoa', force=True)

            clean_scene()

            cmds.playbackOptions(animationStartTime=950, min=950)

            hi_main.switch()

            dst_path = export_path + '/' + shot_name
            if not os.path.isdir(dst_path):
                os.makedirs(dst_path)

            export_wsd = dst_path + '/' + shot_name + '.wsd'
            export(export_wsd)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    start('Y:/test/yangtao/as24y_abc', 'Ep02_s10_sc0010')


    # from Qt.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QMessageBox, QVBoxLayout

    # p = 'D:/yangtao/ytwork/runner/wlf/as24y'
    # import sys
    #
    # p in sys.path or sys.path.append(p)
    #
    # import batch_export_abc
    #
    # batch_export_abc.start()
