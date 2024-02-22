# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/9 22:50
"""
import os.path
import pprint

# !/usr/bin/env python
# -*-coding:utf-8 -*-

import shotgun_api3

sg = shotgun_api3.Shotgun('http://sg.ds.com/',
                          script_name='Generic',
                          api_key="kalyywr~ayDzxsum3bshirqea")

from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path


def unlock_file(file_name):
    del_path = unlock_path(file_name)

def asset_get_shot(project_name, asset_name):
    filters = [["project.Project.name", "is", project_name],
               ["code", "is", asset_name]]
    fields = ["shots"]
    asset_link_shots = sg.find_one("Asset", filters, fields)["shots"]

    shots_name_list = []
    for s in asset_link_shots:
        shots_name_list.append(s["name"])

    return shots_name_list


def get_ani_file_from_shot(project_name, shot_name):
    version_name = "%s.ani.animation" % shot_name
    filters = [["project.Project.name", "is", project_name],
               ["code", "starts_with", version_name]]
    fields = ["code", "sg_path_to_geometry"]
    geo_path_list = []
    for v in sg.find("Version", filters, fields):
        geo_path_list.append(v["sg_path_to_geometry"])

    geo_path_list = sorted(geo_path_list)

    if geo_path_list:
        return geo_path_list[-1]


def get_preview_file_from_shot(project_name, shot_name):
    version_name = "%s.ani.animation" % shot_name
    filters = [["project.Project.name", "is", project_name],
               ["code", "starts_with", version_name]]
    fields = ["code", "sg_path_to_movie"]
    path_list = []
    for v in sg.find("Version", filters, fields):
        path_list.append(v["sg_path_to_movie"])

    path_list = sorted(path_list)

    if path_list:
        return path_list[-1]


def get_shot_from_seq(project_name, seq_name):
    filters = [["project.Project.name", "is", project_name],
               ["code", "is", seq_name]]
    fields = ["shots"]
    seq_link_shots = sg.find_one("Sequence", filters, fields)["shots"]

    shots_name_list = []
    for s in seq_link_shots:
        shots_name_list.append(s["name"])

    return shots_name_list


def get_projcet_files(project_name, shot_start_with, contains):
    #version_name = "%s.ani.animation" % shot_name

    filters = [["project.Project.name", "is", project_name],
              # ["entity.Shot.sg_sequence.Sequence.code", "is", seq_name],
               ["entity.Shot.code", "starts_with", shot_start_with],
               ["code", "contains", contains]]

    fields = ["code", "entity.Shot.code", "sg_path_to_geometry"]

    shot_version_map = {}
    for v in sg.find("Version", filters, fields):
        sg_path_to_geometry = v["sg_path_to_geometry"]
        if sg_path_to_geometry and os.path.isfile(sg_path_to_geometry):
            if v["entity.Shot.code"] in shot_version_map:
                shot_version_map[v["entity.Shot.code"]].append(sg_path_to_geometry)
            else:
                shot_version_map[v["entity.Shot.code"]] = [sg_path_to_geometry]

    all_ver_files = []
    for version_list in shot_version_map.values():
        version_list = sorted(version_list)
        all_ver_files.append(version_list[-1])

    return all_ver_files


if __name__ == '__main__':
    aa = get_file_from_seq("NZT", "i10", ".ani.animation")
    print(aa)