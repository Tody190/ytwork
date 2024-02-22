# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/16 17:51
"""
import pprint

try:
    import maya.cmds as cmds
except:
    pass
import os

from oct.pipeline.shotgun import models, API_SCRIPTS

models.ShotgunModel.use_script(API_SCRIPTS.Generic)

from tk_oct_publish.publish_process.rig import export_rig_shader_data
reload(export_rig_shader_data)
from tk_oct_publish.publish_process.rig import export_preview_data

from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path


class Dialog:
    def __init__(self):
        maya_f = cmds.file(q=True, sceneName=True)
        self.version_dir = os.path.dirname(maya_f)

        self.entity = {"code": os.path.splitext(os.path.basename(maya_f))[0]}
        sourceimages = self.version_dir + "/sourceimages"
        self.d_assets_info = {self.entity["code"]: {"v_dir_imgs": sourceimages}}

        # self.proj_name = project
        # self.entity = None
        # self.sg = models.ShotgunModel.sg_client()
        #
        # scene_name = cmds.file(q=True, sceneName=True)
        # shot_name = os.path.basename(scene_name).split(".", 1)[0]
        #
        # filters = [["name", "is", self.proj_name]]
        # fields = ["sg_unit_scale", "project.Project.name"]
        # self.project = models.Project.filter(filters=filters, fields=fields)[0]
        # self.entity = models.Shot.get(project_name=self.proj_name, code=shot_name)
        #
        # self.version_dir = os.path.dirname(scene_name).replace("\\", "/")
        #
        # self.comp_transform_data = {}


def generate_preview_shader_json():
    dialog = Dialog()

    # export pre camera
    from toolsets.tools.srf.gene import export_asset_cam as eac

    asset_info = dialog.d_assets_info[dialog.entity['code']]
    # asset_info['v_dir_imgs']  I:\...\sourceimages
    pdg = export_preview_data.PreviewDataGenerator(sourceimages_path=asset_info['v_dir_imgs'])

    json_file = os.path.join(dialog.version_dir, 'preview_shaders.json').replace('\\', '/')
    if os.path.isfile(json_file):
        unlock_path(json_file)
    else:
        unlock_path(dialog.version_dir)

    pdg.write_json(json_file)

    lock_path(json_file)
    lock_path(dialog.version_dir)


def generate_rig_shader_json():
    dialog = Dialog()

    json_file = os.path.join(dialog.version_dir, 'rig_shaders.json').replace('\\', '/')
    if os.path.isfile(json_file):
        unlock_path(json_file)

    ersd = export_rig_shader_data.StdProcess(dialog)
    rls = ersd.proceed()

    if os.path.isfile(json_file):
        lock_path(json_file)

    return rls