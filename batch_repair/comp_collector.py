# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/7/11 17:13
"""
import glob
import json
import os
import pprint
import shutil
import traceback

try:
    import maya.cmds as cmds
except:
    pass

from oct.pipeline.shotgun import models, API_SCRIPTS

models.ShotgunModel.use_script(API_SCRIPTS.Generic)
from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path
from tk_oct_publish.publish_process.ani import collect_basic_comp_data
from tk_oct_publish.publish_process.proj_nzt_ani import process_scene_and_collect_comp_data_nzt
#from tk_oct_publish.publish_process.ani import process_scene_and_collect_comp_data
from tk_oct_publish.publish_process.ani import get_to_assembly_status
from tk_oct_publish.publish_process.ani import export_comp_data


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

        self.shot_comp_data = {}


def create_and_unlock(dialog):
    unlock_path(dialog.version_dir)
    shot_components_file = dialog.version_dir + '/shot_components.json'
    if os.path.isfile(shot_components_file):
        unlock_path(shot_components_file)
    else:
        with open(shot_components_file, 'w') as f:
            json.dump({}, f)

    data_path = dialog.version_dir + '/data'
    if os.path.isdir(data_path):
        unlock_path(dialog.version_dir + '/data')
    else:
        os.mkdir(data_path)

    comp_transform = dialog.version_dir + '/data/comp_transform.json'
    if os.path.isfile(comp_transform):
        unlock_path(comp_transform)
    else:
        with open(comp_transform, 'w') as f:
            json.dump({}, f)


def get_dialog(project):
    dialog = Dialog(project=project.upper())
    create_and_unlock(dialog)

    return dialog


def generate_comp(project=None, out_file=None):
    if not project:
        project = os.environ["OCT_PROJECT"]

    dialog = get_dialog(project)

    bcd = collect_basic_comp_data.StdProcess(dialog)
    bcd.proceed()
    print("collect_basic_comp_data_rls")
    #pprint.pprint(dialog.shot_comp_data)

    # if project.upper() == "NZT":
    #     pass
    #     # cp = process_scene_and_collect_comp_data_nzt.StdProcess(dialog)
    #     # process_scene_and_collect_comp_data_nzt_rls = cp.proceed()
    #     # print("process_scene_and_collect_comp_data_nzt")
    #     # print(process_scene_and_collect_comp_data_nzt_rls)
    # else:
    cp = get_to_assembly_status.StdProcess(dialog)
    process_scene_and_collect_comp_data_rls = cp.proceed()
    print("process_scene_and_collect_comp_data")
    print(process_scene_and_collect_comp_data_rls)

    if out_file:
        with open(out_file, 'w') as f:
            json.dump(dialog.shot_comp_data, f, indent=4)
    else:
        ce = export_comp_data.StdProcess(dialog)
        export_comp_data_rls = ce.proceed()
        print("export_comp_data")
        print(export_comp_data_rls)

    lock_path(dialog.version_dir)
    lock_path(dialog.version_dir + '/shot_components.json')
    lock_path(dialog.version_dir + '/data')
    lock_path(dialog.version_dir + '/data/comp_transform.json')


def generate_basic_comp(project):
    # 收集镜头信息
    dialog = Dialog(project)
    bcd = collect_basic_comp_data.StdProcess(dialog)
    bcd.proceed()

    return dialog.shot_comp_data


def output_basic_comp(out_file, project=None):
    if not project:
        project = os.environ["OCT_PROJECT"]

    print("------------")
    print("Project: %s" % project)
    print("------------")

    shot_comp_data = generate_basic_comp(project)

    with open(out_file, 'w') as f:
        json.dump(shot_comp_data, f, indent=4)


def run():
    project = os.environ["OCT_PROJECT"]
    generate_comp(project)


if __name__ == '__main__':
    import glob

    for coral_rig_ma in glob.glob(r"I:\projects\fgt\asset\flg\coral*\rig\coral*.rig.rigging\coral*.ma"):
        print(coral_rig_ma)
    #fields = ["sg_unit_scale", "project.Project.name"]

    # filters = [["name", "is", "bil"]]
    # fields = ["sg_unit_scale", "project.Project.name"]
    # project = models.Project.filter(filters=filters, fields=fields)[0]

    # project = models.Project.get(name="bil", fields=fields)
    # print(project.to_dict())
    # data_file_path = dialog.version_dir + '/shot_components.json'
    # data_file_path_bk = dialog.version_dir + '/shot_components.json.bk'
    # if not os.path.exists(data_file_path_bk):
    #     unlock_path(dialog.version_dir)
    #     shutil.copy2(data_file_path, data_file_path_bk)
    #     lock_path(dialog.version_dir)


    # comp_transform_file_path = dialog.version_dir + '/data/comp_transform.json'
    # comp_transform_file_path_bk = dialog.version_dir + '/data/comp_transform.json.bk'
    # if not os.path.exists(comp_transform_file_path_bk):
    #     unlock_path(dialog.version_dir + '/data')
    #     shutil.copy2(comp_transform_file_path, comp_transform_file_path_bk)
    #     lock_path(dialog.version_dir + '/data')

    # import sys
    # import maya.cmds as cmds
    #
    # p = "W:/projects/nzt/misc/users/yangtao/share_code/comp_collector"
    # p in sys.path or sys.path.append(p)
    # import cc_main
    #
    # reload(cc_main.generate_comp("bil"))
    # #
    #
    # ma_f = r"I:\projects\nzt\shot\n40\n40130\ani\n40130.ani.animation\n40130.ani.animation.v001.ma"
    # cmds.file(new=True, f=True)
    # cmds.file(ma_f, open=True, f=True)
    # cc_main.generate_comp()

    fields = ["sg_unit_scale", "project.Project.name"]
    project = models.Project.get(name="nzt", fields=fields)
    print(project.to_dict())
