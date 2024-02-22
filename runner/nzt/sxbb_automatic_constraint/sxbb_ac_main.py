# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/6/26 17:19
"""
import os
import json

from PySide2 import QtWidgets
from PySide2 import QtCore
import pymel.core as pm
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


root_path = "I:/projects/nzt/asset/chr/c050003sxbb/rig/c050003sxbb.rig.rigging"


def getMayaWindow():
    main_window_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_pointer), QtWidgets.QWidget)


def get_execute_list():
    execute_list = []
    info_file = os.path.join(os.path.dirname(__file__), "execute_info.txt")
    with open(info_file, "r") as f:
        for line in f.readlines():
            execute_list.append((line.split("|")[0].strip(),
                                 line.split("|")[1].strip(),
                                 line.split("|")[2].strip()))
    return execute_list

class Main:
    def __init__(self):
        self.asset_name = 'c050003sxbb'
        self.old_ns = 'c050003sxbb_old'
        self.new_ns = self.asset_name

        self.old_file = root_path + '.v005/c050003sxbb.ma'
        self.old_controller_data = os.path.dirname(self.old_file) + '/controller_data.json'
        self.new_file = root_path + '/c050003sxbb.ma'
        self.new_controller_data = os.path.dirname(self.new_file) + '/controller_data.json'

        self.constraint_nodes_list = []
        self.old_ref_node = None

    def replace_asset(self):
        # 查看资产存不存在
        sel = pm.ls(sl=True)
        if not sel:
            pm.confirmDialog(message=u"请先选中 [%s] 再执行" % self.asset_name, button=['OK'])
            return
        # 找到并修改节点名
        ref_node_name = pm.referenceQuery(sel[0], referenceNode=True)
        if not ref_node_name or not ref_node_name.startswith(self.asset_name):
            pm.confirmDialog(message=u"请先选中 [%s], 且资产为引用资产" % self.asset_name, button=['OK'])
            return

        self.old_ref_node = pm.system.FileReference(ref_node_name)

        self.old_ref_node.replaceWith(self.old_file)
        self.old_ref_node.namespace = self.old_ns
        self.old_ns = self.old_ref_node.namespace
        self.old_ref_node.refNode.unlock()
        self.old_ref_node.refNode.rename('%sRN' % self.old_ns)

        pm.confirmDialog(message=u"！！！ 检查动画是否正确再做下一步 ！！！")

    def auto_tpos(self):
        with open(self.old_controller_data, 'r') as f:
            con_data = json.load(f)
            keyable_ctrl_list = con_data.get('keyable')
            pm.select(clear=True)

        current_frame = pm.currentTime(query=True)

        if keyable_ctrl_list:
            min_time = pm.playbackOptions(q=True, minTime=True)

            pm.currentTime(min_time)
            for c in keyable_ctrl_list.keys():
                ctrl = "%s:%s" % (self.old_ns, c)
                pm.setKeyframe(ctrl)

            tpose_frame = min_time - 50
            pm.currentTime(tpose_frame)
            for c, attrs in keyable_ctrl_list.items():
                ctrl = "%s:%s" % (self.old_ns, c)
                for a, v in attrs.items():
                    attr = "%s.%s" % (ctrl, a)
                    pm.setAttr(attr, v)
                    pm.setKeyframe(attr)

            pm.currentTime(current_frame)
            pm.confirmDialog(message=u"已在第 %s 设置 Tpose" % str(tpose_frame))

    def bacth_constraint(self):
        current_frame = pm.currentTime(query=True)

        # 载入最新资产
        ref_node = pm.createReference(self.new_file, namespace=self.asset_name)
        self.new_ns = ref_node.namespace

        # 移动当前帧到第一帧
        pm.currentTime(1)
        # 批量约束
        errors_info = ""
        for ex_item in get_execute_list():
            old_ctrl = "%s:%s" % (self.old_ns, ex_item[0])
            pm.select(old_ctrl)
            new_ctrl = "%s:%s" % (self.new_ns, ex_item[1])
            pm.select(new_ctrl, add=True)

            self.constraint_nodes_list.extend(pm.mel.eval(ex_item[2]))

            try:
                self.constraint_nodes_list.extend(pm.mel.eval(ex_item[2]))
                print("%s %s %s" % (old_ctrl, new_ctrl, ex_item[2]))
            except Exception as e:
                print(e)
                e_info = u'无法约束：[%s] -> [%s], [%s]' % (old_ctrl, new_ctrl, ex_item[2])
                print(e_info)
                errors_info += e_info + "\n"

            pm.select(clear=True)

        if errors_info:
            pm.confirmDialog(message=errors_info, button=['OK'])

        pm.currentTime(current_frame)

    def smart_bake(self):
        with open(self.new_controller_data, 'r') as f:
            con_data = json.load(f)
            keyable_ctrl_list = con_data.get('keyable')
            pm.select(clear=True)
            for ctrl in keyable_ctrl_list:
                new_ctrl = "%s:%s" % (self.new_ns, ctrl)
                pm.select(new_ctrl, add=True)

        # 烘焙
        min_time = pm.playbackOptions(q=True, minTime=True)
        max_time = pm.playbackOptions(q=True, maxTime=True)
        pm.bakeResults(t='%s:%s' % (str(min_time), str(max_time)), smart=True, simulation=True)

        # 删除约束
        for c in self.constraint_nodes_list:
            pm.delete(c)

    def remove_old(self):
        if not self.old_ref_node:
            sel = pm.ls("%s:*" % self.old_ns)
            if not sel:
                return
            old_ref_name = pm.referenceQuery(sel[0], referenceNode=True)
            self.old_ref_node = pm.system.FileReference(old_ref_name)

        if self.old_ref_node:
            self.old_ref_node.remove()


class MainUI(QtWidgets.QWidget):
    def __init__(self):
        super(MainUI, self).__init__()
        self.setParent(getMayaWindow(), QtCore.Qt.Window)
        # self.setMinimumWidth(160)

        self.replace_asset_btn = QtWidgets.QPushButton(u'替换为老版本资产')
        self.auto_tpose_btn = QtWidgets.QPushButton(u'为原绑定前50帧添加Tpos')
        self.constraint_btn = QtWidgets.QPushButton(u'载入新资产并批量约束')
        self.smart_bake_btn = QtWidgets.QPushButton(u'智能烘焙并删除约束')
        self.remove_old_btn = QtWidgets.QPushButton(u'移除旧版')

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.replace_asset_btn)
        self.layout.addWidget(self.auto_tpose_btn)
        self.layout.addWidget(self.constraint_btn)
        self.layout.addWidget(self.smart_bake_btn)
        self.layout.addWidget(self.remove_old_btn)

        self.sam = Main()

        self.replace_asset_btn.clicked.connect(self.sam.replace_asset)
        self.auto_tpose_btn.clicked.connect(self.sam.auto_tpos)
        self.constraint_btn.clicked.connect(self.sam.bacth_constraint)
        self.smart_bake_btn.clicked.connect(self.sam.smart_bake)
        self.remove_old_btn.clicked.connect(self.sam.remove_old)
