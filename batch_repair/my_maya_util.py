# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/22 14:20
"""
import os.path

import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel


def remove_unused_namespaces():
    import maya.cmds as cmds

    # 获取所有命名空间
    all_namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)

    # 获取正在使用的命名空间
    used_namespaces = set()
    for node in cmds.ls(dag=True, long=True):
        try:
            namespace = cmds.referenceQuery(node, namespace=True)
        except:
            namespace = None
        if namespace:
            used_namespaces.add(namespace)

    # 找到未使用的命名空间
    unused_namespaces = list(set(all_namespaces) - used_namespaces)

    # 删除未使用的命名空间
    for ns in unused_namespaces:
        try:
            print("remove %s" % ns)
            cmds.namespace(removeNamespace=ns, deleteNamespaceContent=True)
        except:
            pass


def remove_all_animation_layers():
    # 获取所有的动画层
    animation_layers = mc.ls(type="animLayer")

    # 删除所有的动画层
    for layer in animation_layers:
        mc.delete(layer)

    # 在 "Script Editor" 中输出操作完成信息
    print("All animation layers have been deleted.")


def del_all_display_layers():
    # 获取所有的显示层
    display_layers = mc.ls(type="displayLayer")

    # 删除所有的显示层
    for layer in display_layers:
        mc.delete(layer)

    # 在 "Script Editor" 中输出操作完成信息
    print("All display layers have been deleted.")


def replace_reference(ref, new_ref):
    """

    :param ref: athOrRefNode
    :param new_ref:
    :return:
    """
    namespace = os.path.splitext(os.path.basename(new_ref))[0]

    reference_node = pm.FileReference(ref)
    reference_node.replaceWith(new_ref)

    reference_node.namespace = namespace
    reference_node.refNode.unlock()
    reference_node.refNode.rename('%sRN' % namespace)


def clean_scene():
    off_options = ['deformerOption', 'locatorOption', 'unusedNurbsSrfOption', 'nurbsCrvOption',
                   'expressionOption', 'poseOption', 'cachedOption', 'transformOption',
                   'partitionOption', 'kRemovingUnusedBrushes', 'ptConOption', 'unusedSkinInfsOption',
                   'setsOption']

    clean_options = ['nurbsSrfOption', 'displayLayerOption', 'renderLayerOption',
                     'animationCurveOption', 'groupIDnOption',
                     'shaderOption', 'shaderOption', 'ptConOption', 'pbOption', 'snapshotOption',
                     'unitConversionOption', 'referencedOption',
                     'brushOption', 'unknownNodesOption', 'clipOption']
    #
    # if hasattr(self.dialog, 'coco_v'):
    #     off_options.append('unusedSkinInfsOption')
    #     clean_options.remove('unusedSkinInfsOption')

    for option in off_options:
        mc.optionVar(intValue=(option, False))

    for option in clean_options:
        mc.optionVar(intValue=(option, True))

    os.environ['MAYA_TESTING_CLEANUP'] = '1'
    mel.eval('source cleanUpScene.mel')
    mel.eval('cleanUpScene(1)')
    os.environ['MAYA_TESTING_CLEANUP'] = ''

    for option in clean_options:
        mc.optionVar(intValue=(option, False))

    if mc.objExists('defaultLegacyAssetGlobals'):
        mc.lockNode('defaultLegacyAssetGlobals', lock=False)
        mc.delete('defaultLegacyAssetGlobals')