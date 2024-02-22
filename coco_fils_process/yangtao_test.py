#!/usr/bin/env python
# -*- coding:utf-8 -*-


import glob
import re

asset_type_map_dict = {'chr': 'char', 'prp': 'prop', 'asb': 'set', 'env': 'elem'}
w_file_pattern = 'W:/projects/nzt/shot/{0}/{1}/lay/maya/{1}.lay.rough_layout.v???.ma'
blk_w_file_pattern = 'W:/projects/nzt/shot/{0}/{1}/ani/maya/{1}.ani.blocking.v???.ma'
ani_w_file_pattern = 'W:/projects/nzt/shot/{0}/{1}/ani/maya/{1}.ani.animation.v???.ma'
dst_root_folder = 'W:/projects/nzt/misc/depts/ani/coco_work/shot'


def collect_version_files(shot_list):
    w_file_list = []
    for shot in shot_list:
        print(shot)
        seq = shot[:3]
        for pattern in [ani_w_file_pattern, blk_w_file_pattern, w_file_pattern]:
            file_list = glob.glob(pattern.format(seq, shot))
            if file_list:
                break

        file_list = [file_path.replace('\\', '/') for file_path in file_list]
        file_list = sorted(file_list, key=lambda x: int(x.split('/')[-1].split('.')[-2][1:]))
        w_file = file_list[-1]
        print(w_file)


separators = ['requires', 'file -r', 'file -rdi', 'createNode', 'requires', 'currentUnit', 'fileInfo', 'select',
              'connectAttr', 'dataStructure']
def custom_split(sepr_list, str_to_split):
    # create regular expression dynamically
    regular_exp = '(' + '|'.join(map(re.escape, sepr_list)) + ')'
    return re.split(regular_exp, str_to_split)


def custom_split(sepr_list, str_to_split):
    # create regular expression dynamically
    # 依据 sepr_list 将ma文本内容进行切割
    # 保留所有切割部分
    # re.escape 转义可被解释为正则表达式的部分
    regular_exp = '(' + '|'.join(map(re.escape, sepr_list)) + ')'
    return re.split(regular_exp, str_to_split)

def parse_maya_file_to_blocks(ma_file):
    # text = "python is, an easy;language; to, learn."
    content_blocks = []
    separators = ['requires', 'file -r', 'file -rdi', 'createNode', 'requires', 'currentUnit', 'fileInfo', 'select',
                  'connectAttr', 'dataStructure']
    with open(ma_file, 'r') as f:
        content = f.read()
        content_list = custom_split(separators, content)
        #content_blocks = [content_list[0]]
        #print(content_blocks)
        for i in range((len(content_list) - 1) / 2):
            content_blocks.append(content_list[1 + i * 2] + content_list[2 + i * 2])

        print(content_list[0])
        print("--------")
        print(content_list[1])
        print(content_list[2])
        print("--------")
        print(content_list[3])
        print(content_list[4])
    #     return content_blocks
    # return content_blocks


if __name__ == '__main__':
    ma_file = r"D:\code\test\wanjingwei\i10390.ani.blocking.v003.ma"
    aa = parse_maya_file_to_blocks(ma_file)


    # batch_process_file()
    # shot_list = ['i20680', 'i10840']
    # shot_list = ['i20190', 'i10460', 'i10830', 'i10810', 'i10850']
    # shot_list = ['i20160']
    # shot_list = ['i10060', 'i10070', 'i10120', 'i10160', 'i10390']
    # file_list = collect_version_files(shot_list)
