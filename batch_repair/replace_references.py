# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/9 22:43
"""
import os.path

import pymel.core as pm


def replace_asset(org_file, replace_file):
    org_file = org_file.replace('\\', '/')
    replace_file = replace_file.replace('\\', '/')
    namespace = os.path.splitext(os.path.basename(replace_file))[0]

    for ref_n in pm.listReferences():
        if org_file == ref_n.path:
            ref_n.replaceWith(replace_file)
            # 修改名字
            ref_n.namespace = namespace
            ref_n.refNode.unlock()
            ref_n.refNode.rename('%sRN' % namespace)




