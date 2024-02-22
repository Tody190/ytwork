# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/7/11 14:58
"""
import os
import process_nzt_shot_files


def exe():
    print(u"请输入一个标准的可可豆回收工程路径")
    print(u"例如：I:/projects/nzt/from_kekedou/NZT/shots/lzb/lzb003/ani/animation/ok/v001")

    f_path = raw_input(">: ")
    if os.path.exists(f_path):
        f_path = f_path.replace("\\", "/")
        process_nzt_shot_files.run(f_path)


if __name__ == '__main__':
    exe()