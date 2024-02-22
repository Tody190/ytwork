# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/9 22:50
"""
import glob
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


def pub_file_get_version(project_name, pub_file):
    filters = [["project.Project.name", "is", project_name],
               ["sg_path_to_geometry", "is", pub_file]]

    fields = ["code", "entity.Shot.code", "sg_path_to_geometry"]

    return sg.find_one("Version", filters, fields)


def get_projcet_files(project_name, contains, shot_start_with=None):
    # version_name = "%s.ani.animation" % shot_name

    filters = [["project.Project.name", "is", project_name],
               ["code", "contains", contains]]

    if shot_start_with:
        filters += ["entity.Shot.code", "starts_with", shot_start_with],

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


def get_kekedou_shot_name(oct_shot_name):
    proj = {'type': 'Project', 'id': 107}
    shot_e = sg.find_one('Shot', filters=[['project', 'is', proj],
                                          ['code', 'is', oct_shot_name]],
                         fields=['sg_client_shot_name'])
    if shot_e:
        return shot_e['sg_client_shot_name']
    else:
        print("Can not find [%s]" % oct_shot_name)


def get_oct_shot_name(kekedou_shot_name):
    proj = {'type': 'Project', 'id': 107}
    shot_e = sg.find_one('Shot', filters=[['project', 'is', proj],
                                          ['sg_client_shot_name', 'is', kekedou_shot_name]],
                         fields=['code'])
    if shot_e:
        return shot_e['code']
    else:
        print("Can not find [%s]" % kekedou_shot_name)


def get_kekedou_task_name(oct_task_name):
    kekedou_task_name_map = {"animation": "animation",
                             "blocking": "animation",
                             "rough_layout": "lay"}

    for task_name in kekedou_task_name_map:
        if oct_task_name in task_name:
            return kekedou_task_name_map[task_name]


def get_kekedou_version_name(oct_version_name):
    oct_shot_name = oct_version_name.split(".")[0]
    oct_step_name = oct_version_name.split(".")[1]
    oct_task_name = oct_version_name.split(".")[2]
    _oct_ver = "%s.%s.%s" % (oct_shot_name, oct_step_name, oct_task_name)

    kekedou_shot_name = get_kekedou_shot_name(oct_shot_name)
    kekedou_task_name = get_kekedou_task_name(oct_task_name)
    _kekedou_ver = "%s_%s_%s" % (kekedou_shot_name, oct_step_name, kekedou_task_name)

    return oct_version_name.replace(_oct_ver, _kekedou_ver)


def get_shot_frames(project_name, shot_name):
    filters = [["project.Project.name", "is", project_name],
               ["code", "is", shot_name]]

    fields = ["sg_cut_in", "sg_cut_out"]

    shot_e = sg.find_one("Shot", filters, fields)
    if shot_e:
        return shot_e["sg_cut_in"], shot_e["sg_cut_out"]


def get_w_files(project, shot, step_list):
    # W:/projects/bil/shot/n10/n10050/ani/maya"
    seq = shot[:3]
    glob_path = "W:/projects/%s/shot/%s/%s*/" % (project.lower(), seq, shot)

    shot_files_map = {}
    # get shot
    for s_p in glob.glob(glob_path):
        for step in step_list:
            ma_file_glob = s_p + "%s/maya/%s*.%s.*.*.ma" % (step, seq, step)

            ma_files = glob.glob(ma_file_glob)
            if ma_files:
                shot_name = ma_files[0].split("\\")[-1].split(".")[0]
                if shot_name in shot_files_map.keys():
                    shot_files_map[shot_name] = shot_files_map[shot_name] + ma_files
                else:
                    shot_files_map[shot_name] = ma_files

    return shot_files_map


def get_w_max_files(project, seq, step_list, shot=None):
    # W:/projects/bil/shot/n10/n10050/ani/maya"
    glob_path = "W:/projects/%s/shot/%s" % (project.lower(), seq)

    if shot:
        glob_path += "/%s/" % shot
    else:
        glob_path += "/*/"

    shot_files = []
    # get shot
    for s_p in glob.glob(glob_path):
        for step in step_list:
            ma_file_glob = s_p + "%s/maya/%s*.%s.*.*.ma" % (step, seq, step)
            ma_files = glob.glob(ma_file_glob)
            if ma_files:
                if len(ma_files) == 1:
                    m_f = ma_files[0].replace("\\", "/")
                else:
                    sorted_ma_files = sorted(ma_files, key=os.path.getctime, reverse=True)
                    m_f = sorted_ma_files[0].replace("\\", "/")

                if os.path.exists(m_f) and m_f not in shot_files:
                    shot_files.append(m_f)
                break

    return shot_files


def get_translated_data(project_name):
    filters = [["project.Project.name", "is", project_name]]

    fields = ["code", "sg_translated_data"]

    for shot_e in sg.find("Shot", filters, fields):
        data_str = shot_e["sg_translated_data"]
        if data_str:
            for d in eval(data_str):
                if abs(int(d)) > 30000:
                    print(shot_e["code"], data_str)


if __name__ == '__main__':
    get_translated_data("nzt")
