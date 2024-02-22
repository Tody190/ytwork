# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/22 17:15
"""


import maya.cmds as cmds

def recursive_delete(node):
    children = cmds.listRelatives(node, children=True)
    if children:
        for child in children:
            recursive_delete(child)

    cmds.lockNode(node, lock=False)
    cmds.delete(node)

# 替换为你想删除的对象的名称
object_to_delete = "n10160_cam"
recursive_delete(object_to_delete)