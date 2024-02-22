# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/21 15:44
"""

import os
import json
import pprint

from PySide2 import QtWidgets
from PySide2 import QtCore
import pymel.core as pm
import maya.cmds as cmds
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def getMayaWindow():
    main_window_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_pointer), QtWidgets.QWidget)


class Main:
    def __init__(self):
        self.asset_name = 'tianlangxing'
        self.old_ns = self.asset_name + "_old"
        self.new_ns = self.asset_name

        rig_root_path = "I:/projects/fgt/asset/chr/tianlangxing/rig/tianlangxing.rig.rigging_nemo"
        self.old_file = rig_root_path + '.v011/tianlangxing.ma'
        self.new_file = rig_root_path + '/tianlangxing.ma'

        self.constraint_nodes_list = []
        self.old_ref_node = None
        self.execute_data = []
        self.ctrl_map = {}

    def get_ctrl_map(self):
        # 猜测新旧控制器的映射关系
        for n in cmds.listRelatives(self.old_ns + ":Root_grp", ad=True, c=True):
            anim_curve_list = cmds.listConnections(n, type="animCurve", d=False)
            if anim_curve_list:
                ctrl_name = n.split(":")[-1]
                new_name = "%s:%s" % (self.new_ns, ctrl_name)
                if cmds.objExists(new_name):
                    self.ctrl_map[n] = new_name
                else:
                    new_name += "_ctrl"
                    if cmds.objExists(new_name):
                        self.ctrl_map[n] = new_name
                    else:
                        print("No exist: ", new_name)

        # pprint.pprint(self.ctrl_map)

    def reconnect_anim(self):
        self.get_ctrl_map()
        for old_ctrl, new_ctrl in self.ctrl_map.items():
            new_ctrl = self.ctrl_map[old_ctrl]
            animcurve_connection_list = cmds.listConnections(old_ctrl, type="animCurve", d=False, p=True, c=True)
            if not animcurve_connection_list:
                continue
            # [当前节点属性，连入的属性，。。。]
            for i, old_ctrl_attr in enumerate(animcurve_connection_list):
                # old_ctrl_attr = tianlangxing_old:Mouth_second8_Con.tx
                n = i + 1
                if n % 2 != 0:
                    # old_ctrl = old_ctrl_attr.split(":")[-1].split(".")[0]  # Mouth_second8_Con
                    old_attr = old_ctrl_attr.split(":")[-1].split(".")[-1]  # tx

                    output_attr = animcurve_connection_list[i + 1]
                    new_ctrl_attr = new_ctrl + "." + old_attr

                    if cmds.objExists(output_attr) and cmds.objExists(new_ctrl_attr):
                        if not cmds.isConnected(output_attr, new_ctrl_attr):
                            try:
                                cmds.connectAttr(output_attr, new_ctrl_attr, f=True)
                            except Exception as e:
                                print("Error: %s ==> %s:" % (output_attr, new_ctrl_attr), e)

        pm.confirmDialog(message=u"！！！ 如失败，请合并动画层再操作 ！！！")

    def load_assets(self):
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

        # 载入最新资产
        ref_node = pm.createReference(self.new_file, namespace=self.asset_name)
        self.new_ns = ref_node.namespace

        msg = u"检查动画是否正确再做下一步 ！！！\n"
        msg += u"检查动画无误后合并动画层再做下一步 ！！！\n"
        pm.confirmDialog(message=msg)

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
        self.sam = Main()

        self.setParent(getMayaWindow(), QtCore.Qt.Window)

        self.setWindowTitle(self.sam.asset_name)

        self.load_assets_btn = QtWidgets.QPushButton(u'载入[%s]资产' % self.sam.asset_name)
        self.reconnect_anim_btn = QtWidgets.QPushButton(u'将旧版资产动画连接到新版')
        self.remove_old_btn = QtWidgets.QPushButton(u'移除旧版资产')

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.load_assets_btn)
        self.layout.addWidget(self.reconnect_anim_btn)
        self.layout.addWidget(self.remove_old_btn)

        self.load_assets_btn.clicked.connect(self.sam.load_assets)
        self.reconnect_anim_btn.clicked.connect(self.sam.reconnect_anim)
        self.remove_old_btn.clicked.connect(self.sam.remove_old)


if __name__ == '__main__':
    pass
# p = "W:/projects/nzt/misc/users/yangtao/main_code"
# import sys
#
# p in sys.path or sys.path.append(p)
#
# from runner.fgt.tlx_automatic_constraint import tlx_ac_main
#
# reload(tlx_ac_main)
# tam = tlx_ac_main.MainUI()
# tam.show()