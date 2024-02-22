#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 16:01
# @Author  : YangTao
# @File    : cgtw_temp.py


import pprint
import json

import cgtw2

t_tw = cgtw2.tw()


def get_all_fields(database, module, module_type):
    # 获取所有的 filed 和 字段中文名
    if module_type == "task":
        for field_data in t_tw.task.fields_and_str(database, module):
            return field_data


def get_id(database, module, module_type, filter_list=None):
    # 获取实体 id
    if filter_list is None:
        filter_list = []
    if module_type == "task":
        return t_tw.task.get_id(database, module, filter_list)


def get_data(database, module, module_type, filter_list=None, field_sign_list=None):
    # 获取实体数据
    if filter_list is None:
        filter_list = []
    if field_sign_list is None:
        field_sign_list = []
    if module_type == "task":
        # 要获取项的数据得通过 id，得通过id 获取数据
        id_list = get_id(database,
                         module,
                         module_type,
                         filter_list=filter_list)
        return t_tw.task.get(database, module, id_list, field_sign_list)


def get_sign_filebox(database, module, module_type, id, filebox_sign):
    # 获取 filebox id
    if module_type == "task":
        return t_tw.task.get_sign_filebox(database, module, id, filebox_sign)


if __name__ == '__main__':
    the_database = "proj_text_cg_v04"
    the_module = "shot"
    the_module_type = "task"
    task_id = "BAB9525B-1C36-42C3-E706-49BDCEA72704"

    # get_all_fields(the_database, the_module, the_module_type)

    # filter 的 写法参考cgtw文档的过滤条件运算符和参数
    # the_filter_list = [["shot.entity", "=", "sc01_sh01"], "and",
    #                    ["pipeline.entity", "=", "effect_project"]]
    #
    # # field 与 shotgun 写法一致
    # the_field_sign_list = ["shot.entity", "pipeline.entity"]
    # data = get_data(the_database,
    #                 the_module,
    #                 the_module_type,
    #                 filter_list=the_filter_list,
    #                 field_sign_list=the_field_sign_list)
    # pprint.pprint(data)

    # 获取文件筐 id
    filebox_sign = get_sign_filebox(the_database,
                                    the_module,
                                    the_module_type,
                                    task_id,
                                    filebox_sign="gejdge")

    pprint.pprint(filebox_sign)
