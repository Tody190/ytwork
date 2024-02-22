# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/27 17:47
"""
import re

"""
替换旧版的动画资产到新版的
因为旧版资产的控制器是没有 _ctrl 的
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

from batch_repair import my_maya_util


def getMayaWindow():
    main_window_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_pointer), QtWidgets.QWidget)


assets_map = {
    "tianlangxing": ("I:/projects/fgt/asset/chr/tianlangxing/rig/tianlangxing.rig.rigging_nemo.v011/tianlangxing.ma",
                     "I:/projects/fgt/asset/chr/tianlangxing/rig/tianlangxing.rig.rigging_nemo/tianlangxing.ma"),
    "dsf_HT_ShangC_a_RIG": ("Z:/DS/Temp/dsf/Asset/CH/HT_ShangC_a/rig/HT_ShangC_a.rig.RIG/HT_ShangC_a.ma",
                            "I:/projects/fgt/asset/chr/ht_haita_a/rig/ht_haita_a.rig.rigging/ht_haita_a.ma"),
    "dsf_HT_ZhenS_RIG": ("Z:/DS/Temp/dsf/Asset/CH/HT_ZhenS/rig/HT_ZhenS.rig.RIG/HT_ZhenS.ma",
                         "I:/projects/fgt/asset/chr/ht_haita_a/rig/ht_haita_a.rig.rigging/ht_haita_a.ma")}


class Main:
    def __init__(self,
                 asset_namespace,
                 new_reference,
                 old_reference=None):
        self.asset_name = asset_namespace
        self.old_ns = self.asset_name + "_old"
        self.new_ns = self.asset_name

        self.old_file = old_reference
        self.new_file = new_reference

        self.constraint_nodes_list = []
        self.old_ref_node = self.old_ns + "RN"
        self.execute_data = []
        self.ctrl_map = {}

    def get_ctrl_map(self):
        # 猜测新旧控制器的映射关系
        top_node = pm.referenceQuery(self.old_ref_node, nodes=True)[0]
        for n in cmds.listRelatives(top_node, ad=True, c=True):
            n = cmds.ls(n)[0]
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

        # if not ref_node_name or not self.asset_name in ref_node_name:
        #     pm.confirmDialog(message=u"请先选中 [%s], 且资产为引用资产" % self.asset_name, button=['OK'])
        #     return

        self.old_ref_node = pm.system.FileReference(ref_node_name)
        print("old_ref_node", self.old_ref_node)

        if self.old_file:
            self.old_ref_node.replaceWith(self.old_file)
        self.old_ref_node.namespace = self.old_ns

        self.old_ns = self.old_ref_node.namespace
        print(self.old_ns)
        self.old_ref_node.refNode.unlock()
        self.old_ref_node.refNode.rename('%sRN' % self.old_ns)

        # 载入最新资产
        print("load new file: ", self.new_file)
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
        self.__sam = None

        self.setParent(getMayaWindow(), QtCore.Qt.Window)

        self.setWindowTitle(u"动画资产替换工具")

        self.load_assets_btn = QtWidgets.QPushButton(u'载入资产')
        self.reconnect_anim_btn = QtWidgets.QPushButton(u'将旧版资产动画连接到新版')
        self.remove_old_btn = QtWidgets.QPushButton(u'移除旧版资产')

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.load_assets_btn)
        self.layout.addWidget(self.reconnect_anim_btn)
        self.layout.addWidget(self.remove_old_btn)

        self.load_assets_btn.clicked.connect(self.load_assets)
        self.reconnect_anim_btn.clicked.connect(self.reconnect_anim)
        self.remove_old_btn.clicked.connect(self.remove_old)

    @property
    def sam(self):
        if not self.__sam:
            sel = pm.ls(sl=True)
            if not sel:
                pm.confirmDialog(message=u"请先选中要替换的资产再执行", button=['OK'])
                return

            ref_ns = pm.referenceQuery(sel[0], ns=True)
            asset_name = ref_ns.split(":")[-1]
            asset_name = re.sub(r"\d+$", "", asset_name)
            asset_name = asset_name.replace("_old", "")

            print("--%s--" % asset_name)
            if asset_name in assets_map.keys():
                if len(assets_map[asset_name]) == 1:
                    self.__sam = Main(asset_name,
                                      assets_map[asset_name][0])
                else:
                    self.__sam = Main(asset_name,
                                      assets_map[asset_name][0],
                                      assets_map[asset_name][1])
            else:
                message = u"只有以下资产可以执行转换\n%s\n" % "\n".join(assets_map.keys())
                message += u"当前选中的是：%s" % asset_name
                pm.confirmDialog(message=message,
                                 button=['OK'])

        return self.__sam

    def load_assets(self):
        if self.sam:
            self.sam.load_assets()

    def reconnect_anim(self):
        if self.sam:
            self.sam.reconnect_anim()

    def remove_old(self):
        if self.sam:
            self.sam.remove_old()


def replace_ht():
    #my_maya_util.clean_scene()

    sel_objs = pm.ls(sl=True)
    if not sel_objs:
        pm.confirmDialog(message=u"请先选中要替换的资产再执行", button=['OK'])
        return

    for sel in sel_objs:
        ref_ns = pm.referenceQuery(sel, ns=True)
        asset_name = ref_ns.split(":")[-1]
        asset_name = re.sub(r"\d+$", "", asset_name)
        asset_name = asset_name.replace("_old", "")

        rep_m = Main(asset_name, "I:/projects/fgt/asset/chr/ht_haita_a/rig/ht_haita_a.rig.rigging/ht_haita_a.ma")
        rep_m.load_assets()
        rep_m.reconnect_anim()
        rep_m.remove_old()



if __name__ == '__main__':
    pass
# p = "Z:/OCT/TEC/yangtao/main_code"
#
# import sys
#
# p in sys.path or sys.path.append(p)
# from runner.fgt import assets_replace
#
# reload(assets_replace)
#
# mui = assets_replace.MainUI()
# mui.show()
