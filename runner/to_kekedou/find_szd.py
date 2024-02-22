# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/18 11:33
"""
import pprint
import re

import project_files
from coco_fils_process import to_kekedou

shot_list = ['i20390', 'i20440', 'i20460', 'i20470', 'i20480', 'i20490', 'i20520', '20540', 'i20580', 'i20600',
             'i20610', 'i20620', 'i20640', 'i20660', 'i20700', 'i20720', 'i20730', '20750', 'i20770', 'i20780',
             'i20820', 'i20880', 'i20890', 'i20900', 'i20910', 'i20930', 'i20950', 'i20995']


# get all publish file

def get_szd():
    publish_files = []
    for s in shot_list:
        publish_files += project_files.get_projcet_files("nzt", s + ".ani.animation")
        publish_files += project_files.get_projcet_files("nzt", s + ".lay.rough_layout")

    print(publish_files)

    shot_szd_info = {}
    for s_f in publish_files:
        print("------------", s_f)
        shot_szd_info[s_f] = []
        try:
            otok = to_kekedou.OCTToKEKEDOU(s_f)
            b_list = otok.blocks_list
        except Exception as e:
            b_list = []
            print(e)

        for b in b_list:
            if 'file -r -ns "c049002szddb' in b:
                reference_file = re.findall(r"\"[a-zA-Z]+\"[\s\S]* \"(.+?)\"", b)[0]
                print("c049002szddb", reference_file)
                shot_szd_info[s_f].append("c049002szddb")
            elif 'file -r -ns "c049003szddbbl' in b:
                reference_file = re.findall(r"\"[a-zA-Z]+\"[\s\S]* \"(.+?)\"", b)[0]
                print("c049003szddbbl", reference_file)
                shot_szd_info[s_f].append("c049003szddbbl")

    print(shot_szd_info)


shot_szd_info = {'I:/projects/nzt/shot/i20/i20700/ani/i20700.ani.animation.v008/i20700.ani.animation.v008.ma': [],
                 'I:/projects/nzt/shot/i20/i20390/lay/i20390.lay.rough_layout.v019/i20390.lay.rough_layout.v019.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20750/lay/i20750.lay.rough_layout.v007/i20750.lay.rough_layout.v007.ma': [],
                 'I:/projects/nzt/shot/i20/i20910/ani/i20910.ani.animation.v003/i20910.ani.animation.v003.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20720/lay/i20720.lay.rough_layout.v023/i20720.lay.rough_layout.v023.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20480/ani/i20480.ani.animation.v005/i20480.ani.animation.v005.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20730/lay/i20730.lay.rough_layout.v005/i20730.lay.rough_layout.v005.ma': [],
                 'I:/projects/nzt/shot/i20/i20780/lay/i20780.lay.rough_layout.v008/i20780.lay.rough_layout.v008.ma': [],
                 'I:/projects/nzt/shot/i20/i20580/ani/i20580.ani.animation.v004/i20580.ani.animation.v004.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20490/lay/i20490.lay.rough_layout.v020/i20490.lay.rough_layout.v020.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20460/ani/i20460.ani.animation.v012/i20460.ani.animation.v012.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/g20/g20540/lay/g20540.lay.rough_layout.v003/g20540.lay.rough_layout.v003.ma': [],
                 'I:/projects/nzt/shot/i20/i20995/ani/i20995.ani.animation.v007/i20995.ani.animation.v007.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20520/ani/i20520.ani.animation.v015/i20520.ani.animation.v015.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20820/lay/i20820.lay.rough_layout.v011/i20820.lay.rough_layout.v011.ma': [],
                 'I:/projects/nzt/shot/i20/i20660/lay/i20660.lay.rough_layout.v011/i20660.lay.rough_layout.v011.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20600/lay/i20600.lay.rough_layout.v013/i20600.lay.rough_layout.v013.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20770/ani/i20770.ani.animation.v003/i20770.ani.animation.v003.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20820/ani/i20820.ani.animation.v003/i20820.ani.animation.v003.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20440/ani/i20440.ani.animation.v006/i20440.ani.animation.v006.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20930/ani/i20930.ani.animation.v047/i20930.ani.animation.v047.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20730/ani/i20730.ani.animation.v003/i20730.ani.animation.v003.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20610/lay/i20610.lay.rough_layout.v027/i20610.lay.rough_layout.v027.ma': [],
                 'I:/projects/nzt/shot/i20/i20540/ani/i20540.ani.animation.v006/i20540.ani.animation.v006.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20600/ani/i20600.ani.animation.v004/i20600.ani.animation.v004.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20640/lay/i20640.lay.rough_layout.v015/i20640.lay.rough_layout.v015.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20890/ani/i20890.ani.animation.v005/i20890.ani.animation.v005.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20620/ani/i20620.ani.animation.v004/i20620.ani.animation.v004.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20580/lay/i20580.lay.rough_layout.v026/i20580.lay.rough_layout.v026.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20540/lay/i20540.lay.rough_layout.v023/i20540.lay.rough_layout.v023.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20950/lay/i20950.lay.rough_layout.v016/i20950.lay.rough_layout.v016.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20490/ani/i20490.ani.animation.v023/i20490.ani.animation.v023.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20770/lay/i20770.lay.rough_layout.v010/i20770.lay.rough_layout.v010.ma': [],
                 'I:/projects/nzt/shot/i20/i20750/ani/i20750.ani.animation.v006/i20750.ani.animation.v006.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/g20/g20750/lay/g20750.lay.rough_layout.v003/g20750.lay.rough_layout.v003.ma': [],
                 'I:/projects/nzt/shot/i20/i20390/ani/i20390.ani.animation.v012/i20390.ani.animation.v012.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20890/lay/i20890.lay.rough_layout.v009/i20890.lay.rough_layout.v009.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20620/lay/i20620.lay.rough_layout.v044/i20620.lay.rough_layout.v044.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20720/ani/i20720.ani.animation.v002/i20720.ani.animation.v002.ma': [],
                 'I:/projects/nzt/shot/i20/i20700/lay/i20700.lay.rough_layout.v014/i20700.lay.rough_layout.v014.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20995/lay/i20995.lay.rough_layout.v018/i20995.lay.rough_layout.v018.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20910/lay/i20910.lay.rough_layout.v008/i20910.lay.rough_layout.v008.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20930/lay/i20930.lay.rough_layout.v020/i20930.lay.rough_layout.v020.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20780/ani/i20780.ani.animation.v003/i20780.ani.animation.v003.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20900/lay/i20900.lay.rough_layout.v011/i20900.lay.rough_layout.v011.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20900/ani/i20900.ani.animation.v005/i20900.ani.animation.v005.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20880/lay/i20880.lay.rough_layout.v016/i20880.lay.rough_layout.v016.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20880/ani/i20880.ani.animation.v014/i20880.ani.animation.v014.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20610/ani/i20610.ani.animation.v009/i20610.ani.animation.v009.ma': [],
                 'I:/projects/nzt/shot/i20/i20950/ani/i20950.ani.animation.v012/i20950.ani.animation.v012.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20470/ani/i20470.ani.animation.v028/i20470.ani.animation.v028.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20660/ani/i20660.ani.animation.v009/i20660.ani.animation.v009.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20640/ani/i20640.ani.animation.v005/i20640.ani.animation.v005.ma': [
                     'c049002szddb'],
                 'I:/projects/nzt/shot/i20/i20470/lay/i20470.lay.rough_layout.v018/i20470.lay.rough_layout.v018.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20460/lay/i20460.lay.rough_layout.v040/i20460.lay.rough_layout.v040.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20520/lay/i20520.lay.rough_layout.v043/i20520.lay.rough_layout.v043.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20440/lay/i20440.lay.rough_layout.v015/i20440.lay.rough_layout.v015.ma': [
                     'c049003szddbbl'],
                 'I:/projects/nzt/shot/i20/i20480/lay/i20480.lay.rough_layout.v015/i20480.lay.rough_layout.v015.ma': [
                     'c049003szddbbl']}

for s_f, char_list in shot_szd_info.items():
    if char_list and "c049003szddbbl" in char_list and ".ani.animation." in s_f:
        print(s_f, char_list)