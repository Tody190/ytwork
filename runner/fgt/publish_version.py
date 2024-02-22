# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/22 21:13
"""

import os
import glob
import pprint

import shotgun_api3

sg = shotgun_api3.Shotgun('http://sg.ds.com/',
                          script_name='Generic',
                          api_key="kalyywr~ayDzxsum3bshirqea")

from oct.pipeline.shotgun import models, API_SCRIPTS

models.ShotgunModel.use_script(API_SCRIPTS.Generic)
SG = models.ShotgunModel.sg_client()


def create_version(version_dir,
                   version_file,
                   version_name,
                   asset_name,
                   task_name):
    # user = {'type': 'HumanUser', 'login': 'yangtao', 'id': 424}
    asset_entity = models.Asset.get(project_name="FGT", code=asset_name)

    project = {'type': 'Project', 'id': 111}

    filters = [['project', 'is', project],
               ['entity', 'is', {'type': 'Asset', 'id': asset_entity.id}],
               ['content', 'is', task_name]]
    task = models.Task.get(filters=filters)

    # print(task.to_dict())
    # return
    if not task:
        print("No task name %s" % task_name)
        return

    # 修改为 win路径
    local_path = version_dir.replace('/', '\\') + '\\'

    description = "批量提交 v000 版本"

    data = {
        'project': project,
        'entity': asset_entity,
        'sg_task': task,
        'code': version_name,
        'description': description,
        # 'user': user,
        'frame_count': 1,
        'sg_version_type': 'Publish',
        'tag_list': [u'正式'],
        # 'created_by': user,
        'sg_path_to_v_folder': version_dir,
        # 'sg_path_to_movie': preview_file,
        'sg_path_to_geometry': version_file,
        'sg_version_folder': {
            'local_path': local_path,
            'name': version_name,
            'content_type': None,
            'link_type': 'local'
        }
    }
    # print(asset_entity.to_dict())
    # print(task.to_dict())
    filters = [['project', 'is', project],
               ['entity', 'is', asset_entity.to_dict()],
               ['sg_task', 'is', task.to_dict()],
               ['code', 'is', version_name]]

    vs = models.Version.filter(filters=filters)

    # get_v_filters = [['project', 'is', project],
    #                  ['code', 'is', version_name]]

    if not vs:
        v = models.Version.create(**data)
        print('Create: ', version_name)
        print(v.to_dict())

    # v.upload(path=preview_file)


for coral_p in glob.glob("I:/projects/fgt/asset/flg/coral*/mod/coral*.mod.model.v000/*.ma"):
    version_file = coral_p.replace("\\", "/")

    version_dir = os.path.dirname(version_file)
    version_name = version_file.split("/")[7]
    asset_name = version_file.split("/")[5]
    task_name = "model"

    a = [version_file, version_dir, version_name, asset_name, task_name]
    pprint.pprint(a)

    create_version(version_dir,
                   version_file,
                   version_name,
                   asset_name,
                   task_name)

    print("\n")
