# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/8 11:06
"""
import json

import maya.cmds as mc
import maya.mel as mel


class InCamera(object):
    def __init__(self, camera):
        # active editor
        self.camera = camera
        self.__setup_editor()
        self.check_step = 1

    def __setup_editor(self):
        self.active_editor = mc.playblast(ae=1)
        mc.modelEditor(self.active_editor,
                       e=True,
                       allObjects=True,
                       useDefaultMaterial=True,
                       displayAppearance="flatShaded")
        mc.modelEditor(self.active_editor, e=True, )

        # setup plugin, model panel
        if not mc.pluginInfo("viewOverrideMeshID.mll", query=True, loaded=True):
            mc.loadPlugin("viewOverrideMeshID.mll", quiet=True)
        mel.eval("setRendererAndOverrideInModelPanel vp2Renderer OCT_PLAYBLAST {};".format(self.active_editor))

        mc.lookThru(self.active_editor, self.camera)

    def check_one(self, dag_path):
        if not mc.objExists(dag_path):
            return False

        mc.meshIDReset()
        mc.refresh()
        mesh_info = ""
        for item in mc.getMeshIDMap():
            # item is id or full object path
            # if dag_path in item:
            #     return True
            mesh_info += item

        if dag_path in mesh_info:
            return True
        else:
            return False

    def set_shot_components_assemble_value(self,
                                           shot_components_data,
                                           frame_range=None):
        """
        shot_components， the following structure is required：
        {
        component_node_name:{dag_path:"dag_path"}
        ....
        }
        :param frame_range: list, [1001, 1111]
        :param shot_components_data:
        :return:
        """
        shot_components_data = shot_components_data.copy()
        # Set all "to_assemble" values to false
        for comp_node, comp_data in shot_components_data.items():
            comp_data["to_assemble"] = False

        if not frame_range:
            frame_range = [int(mc.playbackOptions(q=True, minTime=True)),
                           int(mc.playbackOptions(q=True, maxTime=True))]

        for current_frame in range(frame_range[0] - self.check_step,
                                   frame_range[1] + self.check_step,
                                   self.check_step):
            mc.currentTime(current_frame)

            mesh_data = []
            for item in mc.getMeshIDMap():
                mesh_data.append(item)

            for comp_node, comp_data in shot_components_data.items():
                if comp_data["to_assemble"]:
                    continue
                if not mc.objExists(comp_data["dag_path"]):
                    continue
                for mesh_dag_path in mesh_data:
                    if comp_data["dag_path"] in mesh_dag_path:
                        comp_data["to_assemble"] = True
                        break

        with open("D:/xx/xxx.json", "w") as f:
            json.dump(shot_components_data, f, indent=4, sort_keys=True)

        return shot_components_data


def test_check():
    import json
    with open("I:/projects/bil/shot/n10/n10070/ani/n10070.ani.animation/shot_components.json", "r") as f:
        shot_components_data = json.load(f)

    ie = InCamera("n10070_cam")
    # dag_path = "|asset|asb|ruins_asb_AR|ruins_asb:Root_grp|ruins_asb:Geo_grp|ruins_asb:grass_grp|ruins_asb:grass_n_grp|ruins_asb:grass_n37_AR"
    # print(ie.check_one(dag_path))
    ie.set_shot_components_assemble_value(shot_components_data)



