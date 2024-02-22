# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/15 11:29
"""

# switch Arm Ik-->Fk
import maya.cmds as mc


def run():
    charName = mc.MGPickerView(q=True, namespace=True) + ':'
    side = 'L_'
    fkShoulderCtrl = charName + side + 'ArmFk01_ctrl'
    fkElbowCtrl = charName + side + 'ArmFk02_ctrl'
    fkWristCtrl = charName + side + 'ArmFk03_ctrl'
    # ikShoulder = charName+ side+'ArmIk01_drv'
    ikElbow = charName + side + 'ArmIk02_drv'
    ikWrist = charName + side + 'ArmIk03_drv'
    ikCtrl = charName + side + 'ArmIk01_ctrl'
    ikElbowCtrl = charName + side + 'ArmPoleVec01_ctrl'
    # Gimbal ctrl
    fkShoulderGimbalCtrl = charName + side + 'ArmFk01Gimbal_ctrl'
    fkWristGimbalCtrl = charName + side + 'ArmFk03Gimbal_ctrl'
    ikGimbalCtrl = charName + side + 'ArmIk01Gimbal_ctrl'
    # state
    armState = charName + side + 'ArmSettings_ctrl.fkIkBlend'
    state = mc.getAttr(armState)

    def ArmIkToFk(fkShoulderCtrl, ikElbow, fkElbowCtrl, fkWristCtrl, ikCtrl, ikWrist):
        # followWorld = mc.getAttr(ikCtrl+'.followWorld')
        # if followWorld == 1.0:
        #	if mc.objExists(fkShoulderCtrl+".followBody"):
        #		mc.setAttr( fkShoulderCtrl+".followBody", 0 )
        #	mc.setAttr( fkShoulderCtrl + ".followWorld", 1 )
        # else:
        #	if mc.objExists(fkShoulderCtrl+".followBody"):
        #		mc.setAttr( fkShoulderCtrl+".followBody", 1 )
        #	mc.setAttr( fkShoulderCtrl+".followWorld", 0 )
        # oc = mc.orientConstraint( ikShoulder, fkShoulderCtrl, offset=[0,0,0], weight=1 )
        rx = mc.getAttr(fkShoulderCtrl + '.rx')
        ry = mc.getAttr(fkShoulderCtrl + '.ry')
        rz = mc.getAttr(fkShoulderCtrl + '.rz')
        if mc.objExists(fkShoulderGimbalCtrl):
            mc.setAttr(fkShoulderGimbalCtrl + '.rx', 0)
            mc.setAttr(fkShoulderGimbalCtrl + '.ry', 0)
            mc.setAttr(fkShoulderGimbalCtrl + '.rz', 0)
        # mc.delete( oc )
        # Deleting the constraint while there are keyframes makes control snap back to original position
        mc.setAttr(fkShoulderCtrl + '.rx', rx)
        mc.setAttr(fkShoulderCtrl + '.ry', ry)
        mc.setAttr(fkShoulderCtrl + '.rz', rz)
        # Temporarily unlock ry and rx
        # setAttr -lock false -keyable true ( fkElbowCtrl + '.rx')
        # setAttr -lock false -keyable true ( fkElbowCtrl + '.ry')
        oc = mc.orientConstraint(ikElbow, fkElbowCtrl, offset=[0, 0, 0], weight=1, skip=['x', 'z'])
        # rx = getAttr ( fkElbowCtrl + '.rx')
        # ry = getAttr ( fkElbowCtrl + '.ry')
        ry = mc.getAttr(fkElbowCtrl + '.ry')
        mc.delete(oc)
        # setAttr ( fkElbowCtrl + '.rx')  rx
        # setAttr ( fkElbowCtrl + '.ry')  ry
        mc.setAttr(fkElbowCtrl + '.ry', ry)
        # setAttr -lock true -keyable false ( fkElbowCtrl + '.rx')
        # setAttr -lock true -keyable false ( fkElbowCtrl + '.ry')
        if mc.objExists(ikGimbalCtrl):
            traGimbal = mc.getAttr(ikGimbalCtrl + '.t')
            rotGimbal = mc.getAttr(ikGimbalCtrl + '.r')
            mc.setAttr(ikGimbalCtrl + '.tx', 0)
            mc.setAttr(ikGimbalCtrl + '.ty', 0)
            mc.setAttr(ikGimbalCtrl + '.tz', 0)
            mc.setAttr(ikGimbalCtrl + '.rx', 0)
            mc.setAttr(ikGimbalCtrl + '.ry', 0)
            mc.setAttr(ikGimbalCtrl + '.rz', 0)
        oc = mc.orientConstraint(ikWrist, fkWristCtrl, offset=[0, 0, 0], weight=1)
        rx = mc.getAttr(fkWristCtrl + '.rx')
        ry = mc.getAttr(fkWristCtrl + '.ry')
        rz = mc.getAttr(fkWristCtrl + '.rz')
        mc.delete(oc)
        mc.setAttr(fkWristCtrl + '.rx', rx)
        mc.setAttr(fkWristCtrl + '.ry', ry)
        mc.setAttr(fkWristCtrl + '.rz', rz)
        if mc.objExists(fkWristGimbalCtrl):
            mc.setAttr(ikGimbalCtrl + '.tx', traGimbal[0][0])
            mc.setAttr(ikGimbalCtrl + '.ty', traGimbal[0][1])
            mc.setAttr(ikGimbalCtrl + '.tz', traGimbal[0][2])
            mc.setAttr(ikGimbalCtrl + '.rx', rotGimbal[0][0])
            mc.setAttr(ikGimbalCtrl + '.ry', rotGimbal[0][1])
            mc.setAttr(ikGimbalCtrl + '.rz', rotGimbal[0][2])
            oc = mc.orientConstraint(ikWrist, fkWristGimbalCtrl, offset=[0, 0, 0], weight=1)
            rx = mc.getAttr(fkWristGimbalCtrl + '.rx')
            ry = mc.getAttr(fkWristGimbalCtrl + '.ry')
            rz = mc.getAttr(fkWristGimbalCtrl + '.rz')
            mc.delete(oc)
            mc.setAttr(fkWristGimbalCtrl + '.rx', rx)
            mc.setAttr(fkWristGimbalCtrl + '.ry', ry)
            mc.setAttr(fkWristGimbalCtrl + '.rz', rz)
        # if( side == ':L'){
        #
        # }
        # if( side == ':R'){
        #	 oc = orientConstraint -offset -180 0 0  ikCtrl  fkWristCtrl
        # }
        # oc = orientConstraikCtrl  fkWristCtrl
        # match length
        length = mc.getAttr(ikCtrl + '.upperArmLength')
        mc.setAttr(fkShoulderCtrl + '.length', length)
        length = mc.getAttr(ikCtrl + '.lowerArmLength')
        mc.setAttr(fkElbowCtrl + '.length', length)

    ArmIkToFk(fkShoulderCtrl, ikElbow, fkElbowCtrl, fkWristCtrl, ikCtrl, ikWrist)
