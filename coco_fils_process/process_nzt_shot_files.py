#!/usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:jiongwan
@team : Octmedia TD Department
@file: process_nzt_shot_files.py 
@time: 2023/02/09
@contact: wanjw126@126.com
"""

"""
此脚本的核心函数是 process_file()
它将文件拷贝一份命名为 *.transfered.ma
替换里面的 scene 文件, (assembly文件)
替换里面相机为 camera_template.ma
替换对应的映射路径
一个问题是, assembly 文件可能是不存在或者路径映射不正确的
但在 batch_process() 使用 这个方法先处理了一下 assembly 文件
还有一个函数 batch_check(), 用于检查可可豆发来的资产是否完整


所以, 这个脚本正确使用流程是这样的:
首先使用 batch_check() 检查发来的资产是否完整
然后使用 batch_process() 批量的将文件复制为  *.transfered.ma, 然后替换相应路径
如果此场有文件需要重传, 再使用 process_file() 单独执行
"""


import os
import re
import glob
import json
import codecs
import ast
import shutil
import shotgun_api3


from oct.pipeline.path import unlock_path
from oct.pipeline.path import lock_path


path_map_dict = {
    '$SERVER_ROOT/': 'I:/projects/nzt/from_kekedou/',
    'N:/': 'I:/projects/nzt/from_kekedou/'
}

default_replace_dict = {
    '$SERVER_ROOT/NZT/assets/set/s040002ctg/assembly/rig/main/ok/s040002ctg_rig_main.ma': 'I:/projects/nzt/asset/asb/s040002ctg/mod/s040002ctg.mod.model/s040002ctg.ma',
    '$SERVER_ROOT/NZT/assets/char/c001002nzTeen/assembly/rig/lay/ok/c001002nzTeen_rig_lay.ma': 'I:/projects/nzt/asset/chr/c001002nzTeen/rig/c001002nzTeen.rig.rigging/c001002nzTeen.ma',
    '$SERVER_ROOT/NZT/assets/set/s041001sea/assembly/rig/main/ok/s041001sea_rig_main.ma': 'I:/projects/nzt/asset/asb/s041001sea/mod/s041001sea.mod.model/s041001sea.ma'
}

sg = shotgun_api3.Shotgun('http://sg.ds.com/', script_name='Generic', api_key='kalyywr~ayDzxsum3bshirqea')
proj = {'type': 'Project', 'id': 107}

asset_type_dict = {'CH': 'chr', 'PROP': 'prp', 'ENV': 'env', 'FLG': 'flg', 'ASB': 'asb'}

# 处理单个文件从可可豆到本地
def process_file(file_path, seq=None, repalce_cam="oct"):
    # content = ''
    # with open(file_path, 'r') as f:
    #     content = f.read()
    # if not os.path.isfile(file_path):
    #     shutil.copy(file_path, file_path + '.bak')
    # else:
    #     shutil.copy(file_path + '.bak', file_path)
    transfered_file = file_path.replace('.ma', '.transfered.ma')
    shutil.copy(file_path, transfered_file)

    # 替换资产的映射表
    # default_replace_dict 好像是一些默认的绑定文件的替换列表
    replace_dict = default_replace_dict.copy()

    scene_file = ''
    # 通过可可豆的镜头号从shotgun获取本地对应的镜头号
    # shot: 本地镜头号, client_shot: 可可豆镜头号
    if seq:
        shot, client_shot = get_shot(transfered_file)
        print("----------------------")
        print("oct_shot", shot)
        print("client_shot", client_shot)
        print("----------------------")
        if shot:
            # 找到 assembly 工程
            scene_file = 'I:/projects/nzt/from_kekedou/NZT/shots/{0}/{1}/assembly/scene/ok/{1}_assembly_scene_ani.transfered.ma'.format(seq, client_shot)

    # 将maya资产部分切分为列表块
    content_blocks = parse_maya_file_to_blocks(transfered_file)

    for block in content_blocks:
        try:
            if block.startswith('file -r'):
                #print("block", block)
                path = block.split(' ')[-1].strip()[:-1][1:-1]
                #print("asset_path: ", path)
                asset_name = path.split('/')[4]
                if 'scene' in path:
                    # 将 scene 文件替换为 transfered scene? 没有判断 scene_file存不存在?
                    replace_dict[path] = scene_file
                else:
                    # 从shotgun找到本地资产路径
                    asset_path = get_asset_path(asset_name)
                    #print(asset_name)
                    if asset_path:
                        replace_dict[path] = asset_path
        except Exception as e:
            print(e)
            print("block", block)

    #print(replace_dict)

    content = ''
    with open(transfered_file, 'r') as tf:
        content = tf.read()
        for src, dst in replace_dict.items():
            content = content.replace(src, dst)

        # 替换相机
        
        if repalce_cam == "oct":
            re_cam = 'W:/projects/nzt/misc/configs/maya/kekedou/camera_template.ma'
        if repalce_cam == "coco":
            re_cam = 'I:/projects/nzt/from_kekedou/NZT/shots/_resources/rig/camRig.ma'
        content = content.replace('N:/NZT/shots/_resources/rig/camRig.ma', re_cam)

        # 将可可都路径替换为本地路径
        for key, value in path_map_dict.items():
            content = content.replace(key, value)

    with open(transfered_file, 'w') as tf:
        tf.write(content)

    print(u"完成", transfered_file)

# 批量
def batch_process(root_folder):
    # I: / projects / nzt / from_kekedou / NZT / shots / cjm / cjm005 / ani / lay / ok
    print('{}/*/*/lay/ok/*_ani_lay.ma'.format(root_folder))
    ani_files = glob.glob('{}/*/*/lay/ok/*_ani_lay.ma'.format(root_folder))
    ani_files = [file_path.replace('\\', '/') for file_path in ani_files]
    seq = root_folder.split('/')[-1]
    print(len(ani_files))

    for file_path in ani_files:
        print(file_path)
        shot, client_shot = get_shot(file_path)
        if shot >= 'g20120':
            scene_file = 'I:/projects/nzt/from_kekedou/NZT/shots/{0}/{1}/assembly/scene/ok/{1}_assembly_scene_ani.ma'.format(
                seq,
                client_shot)
            process_file(scene_file, seq)
            process_file(file_path, seq)

# 批量检查可可豆文件资产完整性,结果输出到某个文件
def batch_check():
    missing_file_list = []
    missing_file_shot_dict = {}
    missing_file_dict = {}
    ma_file_list = glob.glob('I:/projects/nzt/from_kekedou/NZT/shots/mls/mls*/ani/lay/ok/mls*_ani_lay.ma')
    for file_path in ma_file_list:
        file_path = file_path.replace('\\', '/')
        file_list, shot = process_nzt_shot_file(file_path)
        missing_file_dict[shot] = file_list
        missing_file_list.extend(file_list)

    content = ''
    missing_file_list = list(set(missing_file_list))
    for file_path in missing_file_list:
        print(file_path)
        shot_list = []
        for shot, file_list in missing_file_dict.items():
            if file_path in file_list:
                shot_list.append(shot)

        file_path = file_path.replace('I:/projects/nzt/from_kekedou/', '$SERVER_ROOT/')
        missing_file_shot_dict[file_path] = shot_list
        # content += file_path + ';' +  \n'

    for file_path, shot_list in missing_file_shot_dict.items():
        content += '{}: {}\n\n'.format(file_path, shot_list)

    with codecs.open('D:/yangtao/log/lzb_missing_files.txt', 'w') as f:
        # json.dump(missing_file_shot_dict, f)
        f.write(content)

# 检查资产用, 检查资产中的缓存和贴图是否存在
def process_nzt_shot_file(ma_file):
    print(ma_file)
    blocks = parse_maya_file_to_blocks(ma_file)
    shot = os.path.basename(ma_file).split('_')[0]

    file_list = []
    missing_file_list = []

    for block in blocks:
        if block.startswith('file -r'):
            path = block.split(' ')[-1].strip()[:-1][1:-1]
            print(path)
            file_list.append(path)
            # asset_name = path.split('/')[4]
            # if 'scene' in path and os.path.isfile(scene_file):
            #     replace_dict[path] = scene_file
            # else:
            #     asset_path = get_asset_path(asset_name)
            #     print asset_name
            #     if asset_path:
            #         replace_dict[path] = asset_path
        elif block.startswith('createNode'):
            lines = block.split(';')
            node_type = block.split(' ')[1]
            # print(node_type)
            # if node_type == 'AlembicNode':
            for line in lines:
                # print(line)
                if 'setAttr' in line:
                    tokens = line.strip().split(' ')
                    # print(tokens)
                    # 找到引用的abc缓存
                    if node_type == 'AlembicNode':
                        if tokens[1] == '\".fn\"':
                            path = tokens[-1][1:-1]
                            file_list.append(path)
                    # 找到引用的贴图?
                    elif node_type == 'file':
                        if tokens[1] == '\".ftn\"':
                            path = tokens[-1][1:-1]
                            file_list.append(path)

    local_file_list = []
    # print(file_list)
    for file_path in file_list:
        # print(file_path)
        tokens = file_path.split('/')
        if (file_path.startswith('$SERVER_ROOT/') or file_path.startswith('N:/')):
            for i in range(len(tokens)):
                # ????
                if tokens[i].startswith('v') and tokens[i] != 'view':
                    print('file_path', file_path)
                    tokens.pop(i)
                    break
        file_path = '/'.join(tokens)

        for key, value in path_map_dict.items():
            file_path = file_path.replace(key, value)
        local_file_list.append(file_path)
        if not os.path.isfile(file_path) and not os.path.isfile(file_path.replace('_main_ani', '_main')):
            missing_file_list.append(file_path)

    print(missing_file_list)
    return missing_file_list, shot

# 使用 re 模块将maya文件资产部分块切割
def parse_maya_file_to_blocks(ma_file):
    # text = "python is, an easy;language; to, learn."
    content_blocks = []
    separators = ['requires', 'file -r', 'file -rdi', 'createNode', 'requires', 'currentUnit', 'fileInfo', 'select',
                  'connectAttr', 'dataStructure']
    with open(ma_file, 'r') as f:
        content = f.read()
        content_list = custom_split(separators, content)
        content_blocks = [content_list[0]]
        for i in range(int((len(content_list) - 1) / 2)):
            content_blocks.append(content_list[1 + i * 2] + content_list[2 + i * 2])
        return content_blocks
    return content_blocks

# 使用 re 模块将maya文件资产部分块切割
def custom_split(sepr_list, str_to_split):
    # create regular expression dynamically
    regular_exp = '(' + '|'.join(map(re.escape, sepr_list)) + ')'
    return re.split(regular_exp, str_to_split)

# 获取资产, 先找绑定, 没绑定找模型
def get_asset_path(asset_name):
    asset_e = sg.find('Version', filters=[['entity', 'name_is', asset_name], ['project', 'is', proj],
                                          ['sg_task', 'name_is', 'rigging'], ['sg_version_type', 'is', 'Publish']],
                                 fields=['entity.Asset.sg_asset_type', 'sg_path_to_frames', 'sg_pipeline_type'],
                      order=[{'field_name': 'sg_version_number', 'direction': 'desc'}])
    if not asset_e:
        asset_e = sg.find('Version', filters=[['entity', 'name_is', asset_name], ['project', 'is', proj], ['sg_task', 'name_is', 'model'],
                                              ['sg_version_type', 'is', 'Publish']],
                          fields=['entity.Asset.sg_asset_type', 'sg_path_to_frames', 'sg_pipeline_type'],
                          order=[{'field_name': 'sg_version_number', 'direction': 'desc'}])
        if asset_e:
            asset_type = asset_e[0]['entity.Asset.sg_asset_type']
            return 'I:/projects/nzt/asset/{0}/{1}/mod/{1}.mod.model/{1}.ma'.format(asset_type_dict[asset_type], asset_name)
    else:
        asset_type = asset_e[0]['entity.Asset.sg_asset_type']
        return 'I:/projects/nzt/asset/{0}/{1}/rig/{1}.rig.rigging/{1}.ma'.format(asset_type_dict[asset_type], asset_name)

# 通过可可豆文件名从shotgun获取本地资产对应的文件名
def get_shot(file_path):
    file_name = os.path.basename(file_path).split('_')[0]
    print("get_shot: file_name: ", file_name)
    shot_name = sg.find('Shot',
                        filters=[['project', 'is', proj],
                                 ['sg_client_shot_name', 'is', file_name]],
                        fields=['code'])
    print("get_shot: oct_shot_name: ", shot_name)
    if shot_name:
        return shot_name[0]['code'], file_name
    else:
        raise NameError("file_name")


def run(p):
    unlock_path(p)
    for f_name in os.listdir(p):
        if f_name.endswith(u".ma") and not u".transfered." in f_name:
            f = os.path.join(p, f_name)
            process_file(f, seq=f_name[:3])
    lock_path(p)


if __name__ == '__main__':
    pass
    #batch_check()
    # batch_process()
    # process_nzt_shot_file('I:/projects/nzt/from_kekedou/NZT/shots/cjm/cjm017/ani/lay/ok/cjm017_ani_lay.ma')
    # process_file('I:/projects/nzt/from_kekedou/NZT/shots/cjm/cjm019/assembly/scene/ok/cjm019_assembly_scene_ani.ma')
    # process_file('I:/projects/nzt/from_kekedou/NZT/shots/cjm/cjm019/ani/lay/ok/cjm019_ani_lay.ma')
    # batch_process(r'I:/projects/nzt/from_kekedou/NZT/shots/hcs')
    # f = r"I:\projects\nzt\from_kekedou\NZT\shots\mls\mls182\ani\lay\ok\mls182_ani_lay.ma"
    # process_file(f, 'mls')



    # lock_path(files_floder)
    #
    # file_path = r'W:\projects\nzt\misc\feedback\coco\ani\s02\hcs016\hcs016_ani_bk_v002_016.ma'
    # unlock_path(os.path.dirname(file_path))
    # process_file(file_path, seq='hcs')