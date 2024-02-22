#!/usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:jiongwan
@team : Octmedia TD Department
@file: process_ani_file_to_nzt.py 
@time: 2022/12/07
@contact: wanjw126@126.com
"""
import os
import re
import shutil
import glob
import shotgun_api3

asset_type_map_dict = {'chr': 'char', 'prp': 'prop', 'asb': 'set', 'env': 'elem'}
w_file_pattern = 'W:/projects/nzt/shot/{0}/{1}/lay/maya/{1}.lay.rough_layout.v???.ma'
blk_w_file_pattern = 'W:/projects/nzt/shot/{0}/{1}/ani/maya/{1}.ani.blocking.v???.ma'
ani_w_file_pattern = 'W:/projects/nzt/shot/{0}/{1}/ani/maya/{1}.ani.animation.v???.ma'
dst_root_folder = 'W:/projects/nzt/misc/depts/ani/coco_work/shot'


sg = shotgun_api3.Shotgun('http://sg.ds.com/', script_name='Generic', api_key='kalyywr~ayDzxsum3bshirqea')


def get_w_files(shot_list):
    w_fils = {}
    for shot in shot_list:
        # 依次遍历镜头
        seq = shot[:3]  # 取场号
        # 根据路径模板找到符合规范的文件，优先顺序 animation, blocking, rough_layout
        for pattern in [ani_w_file_pattern, blk_w_file_pattern, w_file_pattern]:
            file_list = glob.glob(pattern.format(seq, shot))
            # 只选择最优先环节
            if file_list:
                break

        file_list = [file_path.replace('\\', '/') for file_path in file_list]

        # 按版本号排序，并取最大版本文件
        file_list = sorted(file_list, key=lambda x:int(x.split('/')[-1].split('.')[-2][1:]))
        w_fils[file_list[-1]] = {}
        w_fils[file_list[-1]]["seq"] = seq
        w_fils[file_list[-1]]["shot"] = shot

    return w_fils


def collect_version_files(shot_list=None, w_files=None):
    """
    收集所有符合镜头号的动画文件
    收集的文件类型优先级为：animation, blocking, rough_layout
    :param w_files:
    :param shot_list:
    :return:
    """
    if not w_files and shot_list:
        w_files = get_w_files(shot_list)

    w_file_list = []

    for w_file,  w_file_info in w_files.items():
        print("**%s**" % str(w_file_info))
        # 找到或者创建给可可豆的镜头文件目录
        # W:/projects/nzt/misc/depts/ani/coco_work/shot/i10060
        dst_folder = os.path.join(dst_root_folder, w_file_info["shot"]).replace('\\', '/')
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        # 拷贝最新版的工程文件到coco_work目录
        shutil.copy2(w_file, dst_folder)
        print("%s ==> %s" % (w_file, dst_folder))

        # 拷贝最新版的mov到可可豆目录
        for pattern in [ani_w_file_pattern, blk_w_file_pattern, w_file_pattern]:
            mov_list = glob.glob(pattern.format(w_file_info["seq"], w_file_info["shot"]).replace('.ma', '.mov'))
            if mov_list:
                break
        mov_list = [mov_path.replace('\\', '/') for mov_path in mov_list]
        mov_list = sorted(mov_list, key=lambda x: int(x.split('/')[-1].split('.')[-2][1:]))
        mov_file = mov_list[-1]

        shutil.copy2(mov_file, dst_folder)
        print("%s ==> %s" % (mov_file, dst_folder))

        # 拷贝序列图到可可豆目录
        sourceimages = os.path.join(os.path.dirname(w_file), 'sourceimages').replace('\\', '/')
        if os.path.exists(sourceimages):
            copy_and_overwrite(sourceimages, os.path.join(dst_folder, 'sourceimages'))
            # print(os.path.join(dst_folder, 'sourceimages'))
            # shutil.copytree(sourceimages, 'sourceimages')

        cache = os.path.join(os.path.dirname(w_file), 'cache').replace('\\', '/')

        # 拷贝缓存到可可豆目录
        if os.path.exists(cache):
            copy_and_overwrite(cache, os.path.join(dst_folder, 'cache'))
            # print(os.path.join(dst_folder, 'cache'))
            # shutil.copytree(cache, dst_folder)

        w_file_list.append(os.path.join(dst_folder, os.path.basename(w_file)).replace('\\', '/'))

    return w_file_list


def copy_and_overwrite(from_path, to_path):
    # 删除再拷贝
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)
    print("%s ==> %s" % (from_path, to_path))


def process_ani_file_to_nzt(ma_file):
    print("Conver: %s" % ma_file)
    # 将maya文件跟资产相关的逻辑块提取成为列表
    blocks = parse_maya_file_to_blocks(ma_file)
    replace_list = []  # 替换映射列表，[可可豆对应位置，本地文件]

    for block in blocks:
        if block.startswith('file -r'):
            # 获取相应的文件路径
            file_path = block.split('"mayaAscii"')[-1].strip()[1:-2]
            print("------ block -----")
            print("file_path: %s"%file_path)
            # 如果是提交盘
            if file_path.startswith('I:/'):
                if file_path == "I:/projects/nzt/from_kekedou/NZT/shots/_resources/rig/camRig.ma":
                    replace_list.append([file_path, file_path.replace('I:/projects/nzt/from_kekedou', '$SERVER_ROOT')])
                    continue

                tokens = file_path.split('/')
                print("tokens: ", tokens)
                # 获取资产名
                asset_name = tokens[-1].replace('.ma', '')
                print("asset_name: ", asset_name)
                # 获取资产类型
                asset_type = tokens[4]
                print("asset_type: ", asset_type)
                # 获取部门
                step = tokens[-3]
                print("step: ", asset_type)
                # 获取可可豆对应的资产类型
                coco_type = asset_type_map_dict[asset_type]
                print("coco_type: ", asset_type)
                # 拼装from_kekedou的路径
                if step == 'rig':
                    coco_path = 'I:/projects/nzt/from_kekedou/NZT/assets/{asset_type}/{asset_name}/assembly/{step}/main/ok/{asset_name}_rig_main.ma'.format(
                        asset_name=asset_name, asset_type=coco_type, step=step)
                else:
                    coco_path = 'I:/projects/nzt/from_kekedou/NZT/assets/{asset_type}/{asset_name}/{step}/geo/main/ok/{asset_name}_geo_main.ma'.format(
                        asset_name=asset_name, asset_type=coco_type, step=step)

                if not os.path.isfile(coco_path):
                    print("asset_name: %s, asset_type: %s, step:%s" % (asset_name, asset_type, step))
                    print("coco_path is not exist: %s" % coco_path)

                replace_list.append([file_path, coco_path.replace('I:/projects/nzt/from_kekedou', '$SERVER_ROOT')])

    # 渲染的相机模板
    replace_list.append(['W:/projects/nzt/misc/configs/maya/kekedou/camera_template.ma', '$SERVER_ROOT/NZT/shots/_resources/rig/camRig.ma'])
    print("ReplaceMap: %s" % replace_list)

    # 文件备份?备份存在就使用备份?
    if not os.path.isfile(ma_file + '.bak'):
        print(ma_file, "= copy =",ma_file + '.bak')
        shutil.copy(ma_file, ma_file + '.bak')
    else:
        shutil.copy(ma_file + '.bak', ma_file)

    content = ''
    with open(ma_file, 'r') as f:
        content = f.read()

    # 将可可豆工程文件路径替换为本地工程文件路径然后覆盖写入
    for pair in replace_list:
        content = content.replace(pair[0], pair[1])
    with open(ma_file, 'w') as f:
        f.write(content)

    print("new: ", ma_file)


def batch_process_file():
    ma_file_list = glob.glob('E:/workspace/test/ani/nzt/sceneCheck/*.ma')
    for ma_file in ma_file_list:
        process_ani_file_to_nzt(ma_file.replace('\\', '/'))


def parse_maya_file_to_blocks(ma_file):
    """
    最后返回内容为 maya文件头 +（separators + separators的内容），形式如下

    separators=['file -r', 'file -rdi'] 时,解析后的maya文件如下
    [[maya文件头],
    [file -r, (file -r 的内容)],
    [file -r, (file -r 的内容)],
     ....
    [file -rdi, (file -rdi 的内容)]
    ....
    :param ma_file:
    :return:
    """
    content_blocks = []
    separators = ['requires', 'file -r', 'file -rdi', 'createNode', 'requires', 'currentUnit', 'fileInfo', 'select',
                  'connectAttr', 'dataStructure']
    with open(ma_file, 'r') as f:
        content = f.read()
        content_list = custom_split(separators, content)
        # maya文件头
        content_blocks = [content_list[0]]
        # maya所需部分
        for i in range(int((len(content_list) - 1) / 2)):
            content_blocks.append(content_list[1 + i * 2] + content_list[2 + i * 2])
        return content_blocks
    return content_blocks


def custom_split(sepr_list, str_to_split):
    # create regular expression dynamically
    # 依据 sepr_list 将ma文本内容进行切割
    # 保留所有切割部分
    # re.escape 转义可被解释为正则表达式的部分
    regular_exp = '(' + '|'.join(map(re.escape, sepr_list)) + ')'
    return re.split(regular_exp, str_to_split)


def get_shot(coco_shot_name):
    proj = {'type': 'Project', 'id': 107}
    shot_name = sg.find('Shot', filters=[['project', 'is', proj],
                                         ['sg_client_shot_name', 'is', coco_shot_name]],
                        fields=['code'])
    if shot_name:
        return shot_name[0]['code']
    else:
        print("Can not find [%s]" % coco_shot_name)


def oct_shots_process(oct_shot_list):
    print("Copy Files: %s" % oct_shot_list)
    file_list = collect_version_files(oct_shot_list)
    print("\n"*2)
    for file_path in file_list:
        process_ani_file_to_nzt(file_path)


def coco_shots_process(coco_shotlist):
    oct_shot_list = []
    for coco_shot_name in coco_shotlist:
        oct_shot_name = get_shot(coco_shot_name)
        if oct_shot_name:
            print("%s <> %s"%(coco_shot_name, oct_shot_name))
            oct_shot_list.append(oct_shot_name)
        else:
            print("%s <> Null" % coco_shot_name)

    oct_shots_process(oct_shot_list)


def get_oct_shot(id):
    proj = {'type': 'Project', 'id': 107}
    shot_name = sg.find('Shot', filters=[['project', 'is', proj],
                                         ['id', 'is', id]],
                        fields=['code'])
    if shot_name:
        return shot_name[0]['code']
    else:
        print("Can not find [%s]" % id)


def process_one_file_to_nzt(the_file):
    shot_name = os.path.basename(the_file).split(".", 1)[0]

    w_fils = {}
    w_fils[the_file] = {}
    w_fils[the_file]["seq"] = shot_name[:3]
    w_fils[the_file]["shot"] = shot_name

    file_list = collect_version_files(shot_list=None, w_files=w_fils)

    for file_path in file_list:
        process_ani_file_to_nzt(file_path)


if __name__ == '__main__':
    """
     处理动画最新版W盘文件给到可可豆
     拷贝的文件类型为, 最新版的mov, 最新版的工程, 序列, 缓存
     环节优先级为：animation, blocking, rough_layout, (只要优先的)
    """
    # batch_process_file()

    # 用可可豆镜头号执行
    # coco_shots_process(["mls134",
    #                     "mls185", 
    #                     "mls153", 
    #                     "mls157"])
    # 用十月的镜头号执行
    #oct_shots_process(["i10810"])

    cover_path = u"W:/projects/nzt/misc/submit/ani/to CoCo/17场/20230630_mls183_mls184_场景问题/i20870.lay.rough_layout.v025.ma"
    process_one_file_to_nzt(cover_path)

