# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/13 19:59
"""


# -*- coding:utf-8 -*-

import traceback
import os

import maya.cmds as cmds
import pymel.core as pm
from tk_oct_publish.proc import modify_to_kekedou_structure
from tk_oct_publish.proc import ftk_nzt_structure

reload(modify_to_kekedou_structure)
reload(ftk_nzt_structure)



class Dialog:
    def __init__(self, project):
        self.proj_name = project
        self.entity = None
        self.sg = models.ShotgunModel.sg_client()

        scene_name = cmds.file(q=True, sceneName=True)
        shot_name = os.path.basename(scene_name).split(".", 1)[0]

        filters = [["name", "is", self.proj_name]]
        fields = ["sg_unit_scale", "project.Project.name"]
        self.project = models.Project.filter(filters=filters, fields=fields)[0]
        self.entity = models.Shot.get(project_name=self.proj_name, code=shot_name)

        self.version_dir = os.path.dirname(scene_name).replace("\\", "/")

        self.comp_transform_data = {}


# All publish process will use StdProcess as the class name.
class StdProcess:

    def __init__(self, dialog):
        self.dialog = dialog
        self.process_name = u"导出按 KeKeDou 标准重命名的资产文件"
        self.description = u"导出按 KeKeDou 标准重命名的资产文件"
        return

    def proceed(self):


    def get_process_name(self):
        return self.process_name

    def get_description(self):
        return self.description


def export_to_kekedou_file(asset_type, asset_name, step, task_name):
    d_imgs = {'file': {}, 'aiImage': {}}
    for n in pm.ls(type='file'):
        d_imgs['file'][n.nodeName()] = n.getAttr('fileTextureName')
    for n in pm.ls(type='aiImage'):
        d_imgs['aiImage'][n.nodeName()] = n.getAttr('filename')

        n_root = pm.PyNode('|Root_grp'),
        n_geo = pm.PyNode('|Root_grp|Geo_grp')
        n_high = pm.PyNode('|Root_grp|Geo_grp|low')
        n_low =  pm.PyNode('|Root_grp|Geo_grp|low')
        n_root_p = n_root.getParent()

        n_root.setParent(None)

        modify_to_kekedou_structure.modify_to(n_root, n_geo, n_high, n_low, asset_type)

        key, ok_dir = ftk_nzt_structure.get_ok_dir(asset_type, asset_name, step, task_name)
        img_dir = ok_dir.replace('I:/projects/nzt/to_kekedou', '$SERVER_ROOT') + '/sourceimages'

        for n in pm.ls(type='file'):
            n.setAttr('fileTextureName', img_dir + '/' + os.path.basename(d_imgs['file'][n.nodeName()]))
        for n in pm.ls(type='aiImage'):
            n.setAttr('filename', img_dir + '/' + os.path.basename(d_imgs['aiImage'][n.nodeName()]))

        kekedou_dir = asset_info['v_dir'] + '/kekedou'
        if not os.path.isdir(kekedou_dir):
            os.makedirs(kekedou_dir)

        kekedou_ma_file = kekedou_dir + '/' + self.dialog.entity['code'] + '.ma'

        pm.select(asset_info['root'], r=True)
        pm.exportSelected(kekedou_ma_file, force=True, options="v=0;", type="mayaAscii", pr=True, es=True)

        modify_to_kekedou_structure.revert_back(n_geo)

        n_root.setParent(n_root_p)

    for n in pm.ls(type='file'):
        n.setAttr('fileTextureName', d_imgs['file'][n.nodeName()])
    for n in pm.ls(type='aiImage'):
        n.setAttr('filename', d_imgs['aiImage'][n.nodeName()])
