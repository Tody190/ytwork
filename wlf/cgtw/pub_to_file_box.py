#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/11 14:29
# @Author  : YangTao
# @File    : pub_to_file_box.py

import pprint
import traceback
import os

import cgtw2

t_tw = cgtw2.tw()


def publish(database,
            module,
            module_type,
            shot_name,
            pipeline_name,
            filebox_sign,
            version_num_str,
            pub_file_list):
    # version_num_str: str, 001

    # 获取任务 id
    the_filter_list = [["shot.entity", "=", shot_name], "and",
                       ["pipeline.entity", "=", pipeline_name]]
    current_task_id = t_tw.task.get_id(database, module, the_filter_list)[0]
    # 获取文件筐数据
    filebox_data = t_tw.task.get_sign_filebox(database, module, current_task_id, filebox_sign)
    # 这个 filebox_data 可以返回很多数据，包括命名规则以及一些检查项的设置
    # 可以通过这些参数做命名检查
    # print(filebox_data)
    filebox_path = filebox_data['path']
    # 原始文件路径
    file_path_list = [p.replace('\\', '/') for p in pub_file_list]
    # 目标文件路径
    # 其实应该做一些文件命名检查之类的，这里就不检查了，直接用原始文件名
    des_file_path_list = [filebox_path + "/" + os.path.basename(p) for p in pub_file_list]

    pub_data = {"module": module,
                "module_type": module_type,
                "db": database,
                "task_id": current_task_id,
                "filebox_data": filebox_data,
                "file_path_list": file_path_list,
                'des_file_path_list': des_file_path_list,
                'version': version_num_str}
    pprint.pprint(pub_data)

    return cgtw2.tw.send_local_http(database,
                                    module,
                                    u"filebox_bulk_upload_to_filebox",
                                    pub_data,
                                    u"get")


if __name__ == '__main__':
    the_database = "proj_text_cg_v04"
    the_module = "shot"
    the_module_type = "task"
    the_shot_name = "sc01_sh01"
    the_pipeline_name = "effect_project"

    the_filebox_sign = "gejdge"
    the_pub_file_list = [r"D:\temp\text_cg_v04_sc01_sh01_efx_particle_cs_v002.mov"]
    the_version = "003"

    res = publish(the_database,
            the_module,
            the_module_type,
            the_shot_name,
            the_pipeline_name,
            the_filebox_sign,
            version_num_str=the_version,
            pub_file_list=the_pub_file_list)

    if res:
        # 刷新界面
        t_tw.client.refresh_all(the_database, the_module, the_module_type)
        print(u"发布成功")
