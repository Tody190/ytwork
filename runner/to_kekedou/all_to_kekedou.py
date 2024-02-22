# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/10 19:18
"""
import glob
import json
import os.path
import pprint
import re
import shutil

import project_files
from coco_fils_process import to_kekedou

import shotgun_api3

sg = shotgun_api3.Shotgun('http://sg.ds.com/',
                          script_name='Generic',
                          api_key="kalyywr~ayDzxsum3bshirqea")

process_fils_json = "D:/yangtao/work/temp/loast_assets_log/process_log.json"


def run_to_kekedou(task,
                   seq,
                   dst_dir=None,
                   ma_file=True,
                   preview=True,
                   components_json=True,
                   translated_data=False,
                   source_images=True,
                   cache=True,
                   sound=True):
    with open(process_fils_json, "r") as f:
        process_data = json.load(f)

    shot_files = project_files.get_projcet_files("nzt", task, seq)
    for s_f in shot_files:
        if s_f in process_data.keys():
            continue
        else:
            try:
                otok = to_kekedou.OCTToKEKEDOU(s_f)
                otok.oct_to_kekedou(dst_dir=dst_dir,
                                    ma_file=ma_file,
                                    preview=preview,
                                    components_json=components_json,
                                    translated_data=translated_data,
                                    source_images=source_images,
                                    cache=cache,
                                    sound=sound)
                process_data[s_f] = "Success"
            except Exception as e:
                process_data[s_f] = str(e)
                print(e)

            with open(process_fils_json, "w") as f:
                json.dump(process_data, f, indent=4, ensure_ascii=False, sort_keys=True)


def json_error_item(remove_contains=None, save_contains=None, q=True, e=True):
    with open(process_fils_json, "r") as f:
        process_data = json.load(f)

    if save_contains:
        for k, v in process_data.items():
            if save_contains not in v:
                if q:
                    print(k, v)
                if e:
                    process_data.pop(k)

    if remove_contains:
        for k, v in process_data.items():
            if remove_contains in v:
                if q:
                    print(k, v)
                if e:
                    process_data.pop(k)

    with open(process_fils_json, "w") as f:
        json.dump(process_data, f, indent=4, ensure_ascii=False, sort_keys=True)


def find_json_error_item():
    with open(process_fils_json, "r") as f:
        process_data = json.load(f)

    for k, v in process_data.items():
        if v != "Success":
            print(k, v)


def all_to_kekedou_wapper():
    for oct_shot in ["i10", "i20"]:
        for task_code in ["ani.animation", "lay.rough_layout"]:
            run_to_kekedou(task_code, oct_shot)


def some_to_kekedou_wapper():
    lay_shot_code = ['mls001', 'mls002', 'mls003', 'mls004', 'mls005', 'mls006', 'mls007', 'mls008', 'mls009',
                     'mls010',
                     'mls011', 'mls012', 'mls013', 'mls014', 'mls015', 'mls016', 'mls017', 'mls018', 'mls019',
                     'mls020',
                     'mls021', 'mls022', 'mls023', 'mls024', 'mls025', 'mls026', 'mls027', 'mls028', 'mls029',
                     'mls030',
                     'mls031', 'mls032', 'mls033', 'mls034', 'mls035', 'mls036', 'mls037', 'mls038', 'mls039',
                     'mls041',
                     'mls042', 'mls043', 'mls045', 'mls046', 'mls047', 'mls048', 'mls049', 'mls049a', 'mls051',
                     'mls052', 'mls053', 'mls054', 'mls055', 'mls056', 'mls057', 'mls058', 'mls059', 'mls060',
                     'mls061',
                     'mls062', 'mls063', 'mls064', 'mls065', 'mls066', 'mls067', 'mls068', 'mls069', 'mls070',
                     'mls071',
                     'mls072', 'mls073', 'mls074', 'mls075', 'mls076', 'mls077', 'mls079', 'mls080', 'mls081',
                     'mls083',
                     'mls084', 'mls085', 'mls086', 'mls087', 'mls088', 'mls089', 'mls090', 'mls091', 'mls092',
                     'mls093',
                     'mls094', 'mls095', 'mls096', 'mls097', 'mls098', 'mls099', 'mls100', 'mls102', 'mls103',
                     'mls104',
                     'mls105', 'mls106', 'mls107', 'mls108', 'mls109', 'mls110', 'mls111', 'mls112', 'mls113',
                     'mls114',
                     'mls115', 'mls116', 'mls117', 'mls118', 'mls119', 'mls120', 'mls121', 'mls122', 'mls123',
                     'mls124',
                     'mls125', 'mls126', 'mls127', 'mls128', 'mls129', 'mls130', 'mls131', 'mls132', 'mls133',
                     'mls134',
                     'mls135', 'mls136', 'mls137', 'mls138', 'mls139', 'mls140', 'mls141', 'mls142', 'mls143',
                     'mls144',
                     'mls145', 'mls146', 'mls147', 'mls148', 'mls149', 'mls150', 'mls151', 'mls152', 'mls153',
                     'mls154',
                     'mls155', 'mls156', 'mls157', 'mls158', 'mls159', 'mls160', 'mls161', 'mls163', 'mls164',
                     'mls165',
                     'mls166', 'mls167', 'mls168', 'mls169', 'mls170', 'mls171', 'mls172', 'mls173', 'mls174',
                     'mls175',
                     'mls177', 'mls178', 'mls179', 'mls181', 'mls182', 'mls183', 'mls184', 'mls185', 'mls186',
                     'mls187',
                     'mls188', 'mls189', 'mls190', 'mls191', 'mls192', 'mls193', 'mls194', 'mls195', 'mls196',
                     'mls197',
                     'dja030', 'dja031', 'dja032', 'dja033', 'dja034', 'dja035', 'dja036', 'dja037', 'dja038',
                     'dja038a', 'dja039', 'dja040', 'dja041', 'dja042', 'dja043', 'dja044', 'dja045', 'dja046',
                     'dja047', 'dja048', 'dja049', 'dja050', 'dja051', 'dja052', 'dja053', 'dja054', 'dja055',
                     'dja056',
                     'dja057', 'dja058', 'dja059', 'dja060', 'dja067', 'dja068', 'dja069', 'dja070', 'dja071',
                     'dja072',
                     'dja073', 'dja074', 'dja075', 'dja076', 'dja077', 'dja078', 'dja079', 'dja080', 'dja081',
                     'dja082',
                     'dja093', 'dja094', 'dja095', 'dja096', 'dja097', 'dja098', 'dja099', 'dja100', 'dja101',
                     'dja102',
                     'dja103', 'dja104', 'dja105', 'dja106', 'dja107', 'dja108', 'dja109', 'dja110', 'dja111',
                     'dja112',
                     'dja113', 'dja114', 'dja115', 'dja116', 'dja117', 'dja118', 'dja119', 'dja120', 'dja121',
                     'dja122',
                     'dja123', 'dja124', 'dja125', 'dja126', 'dja127', 'dja128', 'dja129', 'dja130', 'dja131',
                     'dja132',
                     'dja133', 'dja135', 'dja136', 'dja137', 'dja138', 'dja139', 'dja140', 'dja141', 'dja142',
                     'dja143',
                     'dja144', 'dja145', 'dja147', 'dja148', 'dja149', 'dja150', 'dja151', 'dja152', 'dja153']
    ani_shot_code = ['mls001', 'mls002', 'mls003', 'mls004', 'mls005', 'mls006', 'mls007', 'mls008', 'mls009',
                     'mls010',
                     'mls011', 'mls012', 'mls013', 'mls014', 'mls015', 'mls016', 'mls017', 'mls018', 'mls019',
                     'mls020',
                     'mls021', 'mls022', 'mls023', 'mls024', 'mls025', 'mls026', 'mls027', 'mls028', 'mls029',
                     'mls030',
                     'mls031', 'mls032', 'mls033', 'mls034', 'mls035', 'mls036', 'mls037', 'mls038', 'mls039',
                     'mls041',
                     'mls042', 'mls043', 'mls045', 'mls046', 'mls047', 'mls048', 'mls049', 'mls049a', 'mls051',
                     'mls052', 'mls053', 'mls054', 'mls055', 'mls056', 'mls057', 'mls058', 'mls059', 'mls060',
                     'mls061',
                     'mls062', 'mls063', 'mls064', 'mls065', 'mls066', 'mls067', 'mls068', 'mls069', 'mls070',
                     'mls071',
                     'mls072', 'mls073', 'mls074', 'mls075', 'mls076', 'mls077', 'mls079', 'mls080', 'mls081',
                     'mls083',
                     'mls084', 'mls085', 'mls086', 'mls087', 'mls088', 'mls089', 'mls090', 'mls091', 'mls092',
                     'mls093',
                     'mls094', 'mls095', 'mls097', 'mls099', 'mls100', 'mls102', 'mls103', 'mls104', 'mls105',
                     'mls106',
                     'mls107', 'mls109', 'mls110', 'mls111', 'mls112', 'mls113', 'mls114', 'mls115', 'mls116',
                     'mls117',
                     'mls118', 'mls119', 'mls120', 'mls121', 'mls122', 'mls123', 'mls124', 'mls125', 'mls126',
                     'mls127',
                     'mls128', 'mls129', 'mls130', 'mls131', 'mls132', 'mls133', 'mls134', 'mls135', 'mls136',
                     'mls138',
                     'mls139', 'mls140', 'mls141', 'mls142', 'mls143', 'mls144', 'mls145', 'mls146', 'mls147',
                     'mls148',
                     'mls149', 'mls150', 'mls151', 'mls152', 'mls153', 'mls154', 'mls155', 'mls156', 'mls157',
                     'mls158',
                     'mls159', 'mls160', 'mls161', 'mls163', 'mls164', 'mls165', 'mls166', 'mls167', 'mls168',
                     'mls169',
                     'mls170', 'mls171', 'mls172', 'mls173', 'mls174', 'mls175', 'mls177', 'mls178', 'mls179',
                     'mls181',
                     'mls182', 'mls183', 'mls184', 'mls185', 'mls186', 'mls187', 'mls188', 'mls189', 'mls190',
                     'mls191',
                     'mls192', 'mls193', 'mls194', 'mls195', 'mls196', 'mls197', 'dja030', 'dja031', 'dja032',
                     'dja033',
                     'dja034', 'dja035', 'dja036', 'dja037', 'dja038', 'dja038a', 'dja039', 'dja040', 'dja041',
                     'dja042', 'dja043', 'dja044', 'dja045', 'dja046', 'dja047', 'dja048', 'dja049', 'dja050',
                     'dja051',
                     'dja052', 'dja053', 'dja054', 'dja055', 'dja056', 'dja057', 'dja058', 'dja059', 'dja060',
                     'dja067',
                     'dja068', 'dja069', 'dja070', 'dja071', 'dja072', 'dja073', 'dja074', 'dja075', 'dja076',
                     'dja077',
                     'dja078', 'dja079', 'dja080', 'dja081', 'dja082', 'dja093', 'dja094', 'dja095', 'dja096',
                     'dja098',
                     'dja099', 'dja100', 'dja101', 'dja102', 'dja103', 'dja104', 'dja105', 'dja106', 'dja107',
                     'dja108',
                     'dja110', 'dja111', 'dja112', 'dja113', 'dja114', 'dja115', 'dja116', 'dja117', 'dja120',
                     'dja121',
                     'dja122', 'dja123', 'dja124', 'dja125', 'dja126', 'dja127', 'dja128', 'dja129', 'dja130',
                     'dja131',
                     'dja132', 'dja133', 'dja135', 'dja137', 'dja140', 'dja141', 'dja142', 'dja147', 'dja150',
                     'dja151',
                     'cjm002', 'cjm003', 'cjm004', 'cjm005', 'cjm006', 'cjm007', 'cjm008', 'cjm009', 'cjm010',
                     'cjm011',
                     'cjm012', 'cjm013', 'cjm014', 'cjm015', 'cjm016', 'cjm017', 'cjm018', 'cjm019', 'cjm020',
                     'cjm021',
                     'cjm022', 'cjm023', 'cjm024', 'cjm025', 'cjm026', 'cjm027', 'cjm028', 'cjm029', 'cjm030',
                     'cjm031',
                     'cjm032', 'cjm033', 'cjm034', 'cjm035', 'cjm036', 'cjm038', 'mls096', 'mls098', 'mls108',
                     'mls137',
                     'dja109', 'dja097', 'dja118', 'dja119', 'dja136', 'dja138', 'dja139', 'dja143', 'dja144',
                     'dja145',
                     'dja148', 'dja149', 'dja152', 'dja153']

    for kkd_shot in ani_shot_code:
        if kkd_shot in ["dja051", "dja136"]:
            task_name = "ani.blocking"
        else:
            task_name = "ani.animation"
        oct_shot = project_files.get_oct_shot_name(kkd_shot)
        print(oct_shot)
        run_to_kekedou(task_name, oct_shot)

    for kkd_shot in lay_shot_code:
        oct_shot = project_files.get_oct_shot_name(kkd_shot)
        print(oct_shot)
        run_to_kekedou("lay.rough_layout", oct_shot)


def fix_cam():
    lay_shot_code = ['mls001', 'mls002', 'mls003', 'mls004', 'mls005', 'mls006', 'mls007', 'mls008', 'mls009',
                     'mls010',
                     'mls011', 'mls012', 'mls013', 'mls014', 'mls015', 'mls016', 'mls017', 'mls018', 'mls019',
                     'mls020',
                     'mls021', 'mls022', 'mls023', 'mls024', 'mls025', 'mls026', 'mls027', 'mls028', 'mls029',
                     'mls030',
                     'mls031', 'mls032', 'mls033', 'mls034', 'mls035', 'mls036', 'mls037', 'mls038', 'mls039',
                     'mls041',
                     'mls042', 'mls043', 'mls045', 'mls046', 'mls047', 'mls048', 'mls049', 'mls049a', 'mls051',
                     'mls052', 'mls053', 'mls054', 'mls055', 'mls056', 'mls057', 'mls058', 'mls059', 'mls060',
                     'mls061',
                     'mls062', 'mls063', 'mls064', 'mls065', 'mls066', 'mls067', 'mls068', 'mls069', 'mls070',
                     'mls071',
                     'mls072', 'mls073', 'mls074', 'mls075', 'mls076', 'mls077', 'mls079', 'mls080', 'mls081',
                     'mls083',
                     'mls084', 'mls085', 'mls086', 'mls087', 'mls088', 'mls089', 'mls090', 'mls091', 'mls092',
                     'mls093',
                     'mls094', 'mls095', 'mls096', 'mls097', 'mls098', 'mls099', 'mls100', 'mls102', 'mls103',
                     'mls104',
                     'mls105', 'mls106', 'mls107', 'mls108', 'mls109', 'mls110', 'mls111', 'mls112', 'mls113',
                     'mls114',
                     'mls115', 'mls116', 'mls117', 'mls118', 'mls119', 'mls120', 'mls121', 'mls122', 'mls123',
                     'mls124',
                     'mls125', 'mls126', 'mls127', 'mls128', 'mls129', 'mls130', 'mls131', 'mls132', 'mls133',
                     'mls134',
                     'mls135', 'mls136', 'mls137', 'mls138', 'mls139', 'mls140', 'mls141', 'mls142', 'mls143',
                     'mls144',
                     'mls145', 'mls146', 'mls147', 'mls148', 'mls149', 'mls150', 'mls151', 'mls152', 'mls153',
                     'mls154',
                     'mls155', 'mls156', 'mls157', 'mls158', 'mls159', 'mls160', 'mls161', 'mls163', 'mls164',
                     'mls165',
                     'mls166', 'mls167', 'mls168', 'mls169', 'mls170', 'mls171', 'mls172', 'mls173', 'mls174',
                     'mls175',
                     'mls177', 'mls178', 'mls179', 'mls181', 'mls182', 'mls183', 'mls184', 'mls185', 'mls186',
                     'mls187',
                     'mls188', 'mls189', 'mls190', 'mls191', 'mls192', 'mls193', 'mls194', 'mls195', 'mls196',
                     'mls197',
                     'dja030', 'dja031', 'dja032', 'dja033', 'dja034', 'dja035', 'dja036', 'dja037', 'dja038',
                     'dja038a', 'dja039', 'dja040', 'dja041', 'dja042', 'dja043', 'dja044', 'dja045', 'dja046',
                     'dja047', 'dja048', 'dja049', 'dja050', 'dja051', 'dja052', 'dja053', 'dja054', 'dja055',
                     'dja056',
                     'dja057', 'dja058', 'dja059', 'dja060', 'dja067', 'dja068', 'dja069', 'dja070', 'dja071',
                     'dja072',
                     'dja073', 'dja074', 'dja075', 'dja076', 'dja077', 'dja078', 'dja079', 'dja080', 'dja081',
                     'dja082',
                     'dja093', 'dja094', 'dja095', 'dja096', 'dja097', 'dja098', 'dja099', 'dja100', 'dja101',
                     'dja102',
                     'dja103', 'dja104', 'dja105', 'dja106', 'dja107', 'dja108', 'dja109', 'dja110', 'dja111',
                     'dja112',
                     'dja113', 'dja114', 'dja115', 'dja116', 'dja117', 'dja118', 'dja119', 'dja120', 'dja121',
                     'dja122',
                     'dja123', 'dja124', 'dja125', 'dja126', 'dja127', 'dja128', 'dja129', 'dja130', 'dja131',
                     'dja132',
                     'dja133', 'dja135', 'dja136', 'dja137', 'dja138', 'dja139', 'dja140', 'dja141', 'dja142',
                     'dja143',
                     'dja144', 'dja145', 'dja147', 'dja148', 'dja149', 'dja150', 'dja151', 'dja152', 'dja153']
    ani_shot_code = ['mls001', 'mls002', 'mls003', 'mls004', 'mls005', 'mls006', 'mls007', 'mls008', 'mls009',
                     'mls010',
                     'mls011', 'mls012', 'mls013', 'mls014', 'mls015', 'mls016', 'mls017', 'mls018', 'mls019',
                     'mls020',
                     'mls021', 'mls022', 'mls023', 'mls024', 'mls025', 'mls026', 'mls027', 'mls028', 'mls029',
                     'mls030',
                     'mls031', 'mls032', 'mls033', 'mls034', 'mls035', 'mls036', 'mls037', 'mls038', 'mls039',
                     'mls041',
                     'mls042', 'mls043', 'mls045', 'mls046', 'mls047', 'mls048', 'mls049', 'mls049a', 'mls051',
                     'mls052', 'mls053', 'mls054', 'mls055', 'mls056', 'mls057', 'mls058', 'mls059', 'mls060',
                     'mls061',
                     'mls062', 'mls063', 'mls064', 'mls065', 'mls066', 'mls067', 'mls068', 'mls069', 'mls070',
                     'mls071',
                     'mls072', 'mls073', 'mls074', 'mls075', 'mls076', 'mls077', 'mls079', 'mls080', 'mls081',
                     'mls083',
                     'mls084', 'mls085', 'mls086', 'mls087', 'mls088', 'mls089', 'mls090', 'mls091', 'mls092',
                     'mls093',
                     'mls094', 'mls095', 'mls097', 'mls099', 'mls100', 'mls102', 'mls103', 'mls104', 'mls105',
                     'mls106',
                     'mls107', 'mls109', 'mls110', 'mls111', 'mls112', 'mls113', 'mls114', 'mls115', 'mls116',
                     'mls117',
                     'mls118', 'mls119', 'mls120', 'mls121', 'mls122', 'mls123', 'mls124', 'mls125', 'mls126',
                     'mls127',
                     'mls128', 'mls129', 'mls130', 'mls131', 'mls132', 'mls133', 'mls134', 'mls135', 'mls136',
                     'mls138',
                     'mls139', 'mls140', 'mls141', 'mls142', 'mls143', 'mls144', 'mls145', 'mls146', 'mls147',
                     'mls148',
                     'mls149', 'mls150', 'mls151', 'mls152', 'mls153', 'mls154', 'mls155', 'mls156', 'mls157',
                     'mls158',
                     'mls159', 'mls160', 'mls161', 'mls163', 'mls164', 'mls165', 'mls166', 'mls167', 'mls168',
                     'mls169',
                     'mls170', 'mls171', 'mls172', 'mls173', 'mls174', 'mls175', 'mls177', 'mls178', 'mls179',
                     'mls181',
                     'mls182', 'mls183', 'mls184', 'mls185', 'mls186', 'mls187', 'mls188', 'mls189', 'mls190',
                     'mls191',
                     'mls192', 'mls193', 'mls194', 'mls195', 'mls196', 'mls197', 'dja030', 'dja031', 'dja032',
                     'dja033',
                     'dja034', 'dja035', 'dja036', 'dja037', 'dja038', 'dja038a', 'dja039', 'dja040', 'dja041',
                     'dja042', 'dja043', 'dja044', 'dja045', 'dja046', 'dja047', 'dja048', 'dja049', 'dja050',
                     'dja051',
                     'dja052', 'dja053', 'dja054', 'dja055', 'dja056', 'dja057', 'dja058', 'dja059', 'dja060',
                     'dja067',
                     'dja068', 'dja069', 'dja070', 'dja071', 'dja072', 'dja073', 'dja074', 'dja075', 'dja076',
                     'dja077',
                     'dja078', 'dja079', 'dja080', 'dja081', 'dja082', 'dja093', 'dja094', 'dja095', 'dja096',
                     'dja098',
                     'dja099', 'dja100', 'dja101', 'dja102', 'dja103', 'dja104', 'dja105', 'dja106', 'dja107',
                     'dja108',
                     'dja110', 'dja111', 'dja112', 'dja113', 'dja114', 'dja115', 'dja116', 'dja117', 'dja120',
                     'dja121',
                     'dja122', 'dja123', 'dja124', 'dja125', 'dja126', 'dja127', 'dja128', 'dja129', 'dja130',
                     'dja131',
                     'dja132', 'dja133', 'dja135', 'dja137', 'dja140', 'dja141', 'dja142', 'dja147', 'dja150',
                     'dja151',
                     'cjm002', 'cjm003', 'cjm004', 'cjm005', 'cjm006', 'cjm007', 'cjm008', 'cjm009', 'cjm010',
                     'cjm011',
                     'cjm012', 'cjm013', 'cjm014', 'cjm015', 'cjm016', 'cjm017', 'cjm018', 'cjm019', 'cjm020',
                     'cjm021',
                     'cjm022', 'cjm023', 'cjm024', 'cjm025', 'cjm026', 'cjm027', 'cjm028', 'cjm029', 'cjm030',
                     'cjm031',
                     'cjm032', 'cjm033', 'cjm034', 'cjm035', 'cjm036', 'cjm038', 'mls096', 'mls098', 'mls108',
                     'mls137',
                     'dja109', 'dja097', 'dja118', 'dja119', 'dja136', 'dja138', 'dja139', 'dja143', 'dja144',
                     'dja145',
                     'dja148', 'dja149', 'dja152', 'dja153']

    # ani_shot_code = ["cjm005"]
    # lay_shot_code = []

    for kkd_shot in ani_shot_code:
        if kkd_shot in ["dja051", "dja136"]:
            task_name = "ani.blocking"
        else:
            task_name = "ani.animation"
        oct_shot = project_files.get_oct_shot_name(kkd_shot)
        print("animation", oct_shot)
        run_to_kekedou(task_name,
                       oct_shot,
                       dst_dir=None,
                       ma_file=True,
                       preview=False,
                       components_json=False,
                       translated_data=False,
                       source_images=False,
                       cache=False,
                       sound=False)

    for kkd_shot in lay_shot_code:
        oct_shot = project_files.get_oct_shot_name(kkd_shot)
        print("rough_layout", oct_shot)
        run_to_kekedou("lay.rough_layout",
                       oct_shot,
                       dst_dir=None,
                       ma_file=True,
                       preview=False,
                       components_json=False,
                       translated_data=False,
                       source_images=False,
                       cache=False,
                       sound=False)


def single_to_kekedou(s_f):
    otok = to_kekedou.OCTToKEKEDOU(s_f)
    otok.oct_to_kekedou()


def blocking_to_kekedou():
    for kkd_shot in ["dja051", "dja136"]:
        oct_shot = project_files.get_oct_shot_name(kkd_shot)
        print(oct_shot)
        run_to_kekedou("ani.blocking", oct_shot)


def only_copy_ani_files(kekedou_shot, task_name):
    dst_root_path = "I:/projects/nzt/to_kekedou/NZT/temps/ma_only/"

    seq = kekedou_shot[:3]
    src_path = "I:/projects/nzt/to_kekedou/NZT/shots/%s/%s/ani/%s/ok" % (seq, kekedou_shot, task_name)
    if not os.path.exists(src_path):
        print(src_path, "not exists")
        return

    dst_path = dst_root_path + "%s/%s/ani/%s/ok" % (seq, kekedou_shot, task_name)
    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)

    # # not cache
    # for file_name in os.listdir(src_path):
    #     if file_name == "cache":
    #         continue

    # ma only
    for file_name in os.listdir(src_path):
        if not file_name.endswith(".ma"):
            continue
        src_file = os.path.join(src_path, file_name)
        dst_file = os.path.join(dst_path, file_name)

        print(src_file, "==>", dst_file)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)
        if os.path.isdir(src_file):
            shutil.copytree(src_file, dst_file)


def only_copy_ani_files_wrapper():
    lay_shot_code = ['mls001', 'mls002', 'mls003', 'mls004', 'mls005', 'mls006', 'mls007', 'mls008', 'mls009',
                     'mls010',
                     'mls011', 'mls012', 'mls013', 'mls014', 'mls015', 'mls016', 'mls017', 'mls018', 'mls019',
                     'mls020',
                     'mls021', 'mls022', 'mls023', 'mls024', 'mls025', 'mls026', 'mls027', 'mls028', 'mls029',
                     'mls030',
                     'mls031', 'mls032', 'mls033', 'mls034', 'mls035', 'mls036', 'mls037', 'mls038', 'mls039',
                     'mls041',
                     'mls042', 'mls043', 'mls045', 'mls046', 'mls047', 'mls048', 'mls049', 'mls049a', 'mls051',
                     'mls052', 'mls053', 'mls054', 'mls055', 'mls056', 'mls057', 'mls058', 'mls059', 'mls060',
                     'mls061',
                     'mls062', 'mls063', 'mls064', 'mls065', 'mls066', 'mls067', 'mls068', 'mls069', 'mls070',
                     'mls071',
                     'mls072', 'mls073', 'mls074', 'mls075', 'mls076', 'mls077', 'mls079', 'mls080', 'mls081',
                     'mls083',
                     'mls084', 'mls085', 'mls086', 'mls087', 'mls088', 'mls089', 'mls090', 'mls091', 'mls092',
                     'mls093',
                     'mls094', 'mls095', 'mls096', 'mls097', 'mls098', 'mls099', 'mls100', 'mls102', 'mls103',
                     'mls104',
                     'mls105', 'mls106', 'mls107', 'mls108', 'mls109', 'mls110', 'mls111', 'mls112', 'mls113',
                     'mls114',
                     'mls115', 'mls116', 'mls117', 'mls118', 'mls119', 'mls120', 'mls121', 'mls122', 'mls123',
                     'mls124',
                     'mls125', 'mls126', 'mls127', 'mls128', 'mls129', 'mls130', 'mls131', 'mls132', 'mls133',
                     'mls134',
                     'mls135', 'mls136', 'mls137', 'mls138', 'mls139', 'mls140', 'mls141', 'mls142', 'mls143',
                     'mls144',
                     'mls145', 'mls146', 'mls147', 'mls148', 'mls149', 'mls150', 'mls151', 'mls152', 'mls153',
                     'mls154',
                     'mls155', 'mls156', 'mls157', 'mls158', 'mls159', 'mls160', 'mls161', 'mls163', 'mls164',
                     'mls165',
                     'mls166', 'mls167', 'mls168', 'mls169', 'mls170', 'mls171', 'mls172', 'mls173', 'mls174',
                     'mls175',
                     'mls177', 'mls178', 'mls179', 'mls181', 'mls182', 'mls183', 'mls184', 'mls185', 'mls186',
                     'mls187',
                     'mls188', 'mls189', 'mls190', 'mls191', 'mls192', 'mls193', 'mls194', 'mls195', 'mls196',
                     'mls197',
                     'dja030', 'dja031', 'dja032', 'dja033', 'dja034', 'dja035', 'dja036', 'dja037', 'dja038',
                     'dja038a', 'dja039', 'dja040', 'dja041', 'dja042', 'dja043', 'dja044', 'dja045', 'dja046',
                     'dja047', 'dja048', 'dja049', 'dja050', 'dja051', 'dja052', 'dja053', 'dja054', 'dja055',
                     'dja056',
                     'dja057', 'dja058', 'dja059', 'dja060', 'dja067', 'dja068', 'dja069', 'dja070', 'dja071',
                     'dja072',
                     'dja073', 'dja074', 'dja075', 'dja076', 'dja077', 'dja078', 'dja079', 'dja080', 'dja081',
                     'dja082',
                     'dja093', 'dja094', 'dja095', 'dja096', 'dja097', 'dja098', 'dja099', 'dja100', 'dja101',
                     'dja102',
                     'dja103', 'dja104', 'dja105', 'dja106', 'dja107', 'dja108', 'dja109', 'dja110', 'dja111',
                     'dja112',
                     'dja113', 'dja114', 'dja115', 'dja116', 'dja117', 'dja118', 'dja119', 'dja120', 'dja121',
                     'dja122',
                     'dja123', 'dja124', 'dja125', 'dja126', 'dja127', 'dja128', 'dja129', 'dja130', 'dja131',
                     'dja132',
                     'dja133', 'dja135', 'dja136', 'dja137', 'dja138', 'dja139', 'dja140', 'dja141', 'dja142',
                     'dja143',
                     'dja144', 'dja145', 'dja147', 'dja148', 'dja149', 'dja150', 'dja151', 'dja152', 'dja153']
    ani_shot_code = ['mls001', 'mls002', 'mls003', 'mls004', 'mls005', 'mls006', 'mls007', 'mls008', 'mls009',
                     'mls010',
                     'mls011', 'mls012', 'mls013', 'mls014', 'mls015', 'mls016', 'mls017', 'mls018', 'mls019',
                     'mls020',
                     'mls021', 'mls022', 'mls023', 'mls024', 'mls025', 'mls026', 'mls027', 'mls028', 'mls029',
                     'mls030',
                     'mls031', 'mls032', 'mls033', 'mls034', 'mls035', 'mls036', 'mls037', 'mls038', 'mls039',
                     'mls041',
                     'mls042', 'mls043', 'mls045', 'mls046', 'mls047', 'mls048', 'mls049', 'mls049a', 'mls051',
                     'mls052', 'mls053', 'mls054', 'mls055', 'mls056', 'mls057', 'mls058', 'mls059', 'mls060',
                     'mls061',
                     'mls062', 'mls063', 'mls064', 'mls065', 'mls066', 'mls067', 'mls068', 'mls069', 'mls070',
                     'mls071',
                     'mls072', 'mls073', 'mls074', 'mls075', 'mls076', 'mls077', 'mls079', 'mls080', 'mls081',
                     'mls083',
                     'mls084', 'mls085', 'mls086', 'mls087', 'mls088', 'mls089', 'mls090', 'mls091', 'mls092',
                     'mls093',
                     'mls094', 'mls095', 'mls097', 'mls099', 'mls100', 'mls102', 'mls103', 'mls104', 'mls105',
                     'mls106',
                     'mls107', 'mls109', 'mls110', 'mls111', 'mls112', 'mls113', 'mls114', 'mls115', 'mls116',
                     'mls117',
                     'mls118', 'mls119', 'mls120', 'mls121', 'mls122', 'mls123', 'mls124', 'mls125', 'mls126',
                     'mls127',
                     'mls128', 'mls129', 'mls130', 'mls131', 'mls132', 'mls133', 'mls134', 'mls135', 'mls136',
                     'mls138',
                     'mls139', 'mls140', 'mls141', 'mls142', 'mls143', 'mls144', 'mls145', 'mls146', 'mls147',
                     'mls148',
                     'mls149', 'mls150', 'mls151', 'mls152', 'mls153', 'mls154', 'mls155', 'mls156', 'mls157',
                     'mls158',
                     'mls159', 'mls160', 'mls161', 'mls163', 'mls164', 'mls165', 'mls166', 'mls167', 'mls168',
                     'mls169',
                     'mls170', 'mls171', 'mls172', 'mls173', 'mls174', 'mls175', 'mls177', 'mls178', 'mls179',
                     'mls181',
                     'mls182', 'mls183', 'mls184', 'mls185', 'mls186', 'mls187', 'mls188', 'mls189', 'mls190',
                     'mls191',
                     'mls192', 'mls193', 'mls194', 'mls195', 'mls196', 'mls197', 'dja030', 'dja031', 'dja032',
                     'dja033',
                     'dja034', 'dja035', 'dja036', 'dja037', 'dja038', 'dja038a', 'dja039', 'dja040', 'dja041',
                     'dja042', 'dja043', 'dja044', 'dja045', 'dja046', 'dja047', 'dja048', 'dja049', 'dja050',
                     'dja051',
                     'dja052', 'dja053', 'dja054', 'dja055', 'dja056', 'dja057', 'dja058', 'dja059', 'dja060',
                     'dja067',
                     'dja068', 'dja069', 'dja070', 'dja071', 'dja072', 'dja073', 'dja074', 'dja075', 'dja076',
                     'dja077',
                     'dja078', 'dja079', 'dja080', 'dja081', 'dja082', 'dja093', 'dja094', 'dja095', 'dja096',
                     'dja098',
                     'dja099', 'dja100', 'dja101', 'dja102', 'dja103', 'dja104', 'dja105', 'dja106', 'dja107',
                     'dja108',
                     'dja110', 'dja111', 'dja112', 'dja113', 'dja114', 'dja115', 'dja116', 'dja117', 'dja120',
                     'dja121',
                     'dja122', 'dja123', 'dja124', 'dja125', 'dja126', 'dja127', 'dja128', 'dja129', 'dja130',
                     'dja131',
                     'dja132', 'dja133', 'dja135', 'dja137', 'dja140', 'dja141', 'dja142', 'dja147', 'dja150',
                     'dja151',
                     'cjm002', 'cjm003', 'cjm004', 'cjm005', 'cjm006', 'cjm007', 'cjm008', 'cjm009', 'cjm010',
                     'cjm011',
                     'cjm012', 'cjm013', 'cjm014', 'cjm015', 'cjm016', 'cjm017', 'cjm018', 'cjm019', 'cjm020',
                     'cjm021',
                     'cjm022', 'cjm023', 'cjm024', 'cjm025', 'cjm026', 'cjm027', 'cjm028', 'cjm029', 'cjm030',
                     'cjm031',
                     'cjm032', 'cjm033', 'cjm034', 'cjm035', 'cjm036', 'cjm038', 'mls096', 'mls098', 'mls108',
                     'mls137',
                     'dja109', 'dja097', 'dja118', 'dja119', 'dja136', 'dja138', 'dja139', 'dja143', 'dja144',
                     'dja145',
                     'dja148', 'dja149', 'dja152', 'dja153']

    print(len(ani_shot_code))
    print(len(lay_shot_code))
    #return

    error_map = {}

    for kekedou_shot in ani_shot_code:
        print(kekedou_shot, "animation")
        try:
            only_copy_ani_files(kekedou_shot, "animation")
        except Exception as e:
            error_map[kekedou_shot] = str(e)

    for kekedou_shot in lay_shot_code:
        print(kekedou_shot, "lay")
        try:
            only_copy_ani_files(kekedou_shot, "lay")
        except Exception as e:
            error_map[kekedou_shot] = str(e)

    pprint.pprint(error_map)

    print("Done")


def blocks_list(ma_file):
    # 将 ma 文件切分为列表
    separators = ["requires", "file -r ", "file -rdi ",
                  "createNode ", "requires ", "currentUnit ",
                  "fileInfo ", "select ", "connectAttr ",
                  "dataStructure ", "// End of "]
    regular_exp = "(" + "|".join(map(re.escape, separators)) + ")"

    with open(ma_file, "r") as f:
        blocks_list = re.split(regular_exp, f.read())

    # ["dataStructure-fmt", ""raw" -as "name=notes_bushes_parShape:string=value"";]
    # ↓
    # ["dataStructure-fmt "raw" -as "name=notes_bushes_parShape:string=value"";]
    new_blocks = []
    skip = False
    for i, b in enumerate(blocks_list):
        if skip:
            skip = False
            continue

        if b in separators:
            skip = True
            new_blocks.append(b + blocks_list[i + 1])
        else:
            new_blocks.append(b)

    return new_blocks


def warriorcrowd_rig_to_kekedou():
    filters = [["project.Project.name", "is", "nzt"],
               ["code", "contains", "warriorcrowd.rig.rigging"],
               ["user", "is", {'type': 'HumanUser', 'id': 424}]]

    fields = ["user", "code", "entity.Asset.code", "sg_path_to_geometry"]

    asset_version_map = {}
    for v in sg.find("Version", filters, fields):
        sg_path_to_geometry = v["sg_path_to_geometry"]
        if sg_path_to_geometry and os.path.isfile(sg_path_to_geometry):
            if v["entity.Asset.code"] in asset_version_map:
                asset_version_map[v["entity.Asset.code"]].append(sg_path_to_geometry)
            else:
                asset_version_map[v["entity.Asset.code"]] = [sg_path_to_geometry]

    pprint.pprint(asset_version_map)

    all_ver_files = []
    for version_list in asset_version_map.values():
        version_list = sorted(version_list)
        all_ver_files.append(version_list[-1])

    for ver_file in all_ver_files:
        asset_data = to_kekedou.get_asset_data(ver_file)
        coco_asset_path = "I:/projects/nzt/to_kekedou/NZT/assets/"
        coco_asset_path += "{asset_type}/{asset_name}/assembly/{step}/oct/ok/"
        coco_asset_path = coco_asset_path.format(asset_name=asset_data["asset_name"],
                                                 asset_type=asset_data["asset_type"],
                                                 step=asset_data["step"])

        coco_asset_f = coco_asset_path + "{asset_name}_rig_oct.ma".format(asset_name=asset_data["asset_name"])

        if not os.path.isdir(coco_asset_path):
            os.makedirs(coco_asset_path)

        print(ver_file, coco_asset_f)
        shutil.copy2(ver_file, coco_asset_f)

        oa_file = ver_file.split("/rig/")[0]
        oa_file += "/crd/{asset_name}.crd.original_agent/{asset_name}.ma".format(asset_name=asset_data["asset_name"])
        coco_oa_path = coco_asset_path + "oa/"
        coco_oa_f = coco_oa_path + "{asset_name}.ma".format(asset_name=asset_data["asset_name"])
        if not os.path.isdir(coco_oa_path):
            os.makedirs(coco_oa_path)

        print(oa_file, coco_oa_f)
        shutil.copy2(oa_file, coco_oa_f)


def warriorcrowd_ani_to_kekedou():
    filters = [["project.Project.name", "is", "nzt"],
               ["code", "contains", "warriorcrowd.ani.animation"]]

    fields = ["code", "entity.Asset.code", "sg_path_to_geometry"]

    asset_task_map = {}
    for v in sg.find("Version", filters, fields):
        sg_path_to_geometry = v["sg_path_to_geometry"]
        task_name = v["code"].split(".v0")[0]
        if sg_path_to_geometry and os.path.isfile(sg_path_to_geometry):
            if task_name in asset_task_map:
                asset_task_map[task_name].append(sg_path_to_geometry)
            else:
                asset_task_map[task_name] = [sg_path_to_geometry]

    all_ver_files = []
    for version_list in asset_task_map.values():
        version_list = sorted(version_list)
        all_ver_files.append(version_list[-1])

    for ver_file in all_ver_files:
        asset_data = to_kekedou.get_asset_data(ver_file)
        clip_name = asset_data["task_name"].split("animation_")[-1]
        coco_clip_path = "I:/projects/nzt/to_kekedou/NZT/assets/"
        coco_clip_path += "{asset_type}/{asset_name}/".format(asset_type=asset_data["asset_type"],
                                                              asset_name=asset_data["asset_name"])
        coco_clip_path += "{step}/clip/{clip_name}/ok/".format(step=asset_data["step"],
                                                               clip_name=clip_name)

        if not os.path.isdir(coco_clip_path):
            os.makedirs(coco_clip_path)

        coco_clip_f = coco_clip_path + "{asset_name}_clip_{clip_name}.ma".format(asset_name=asset_data["asset_name"],
                                                                                 clip_name=clip_name)
        print(ver_file, "===>", coco_clip_f)
        with open(coco_clip_f, "w") as f:
            for b in blocks_list(ver_file):
                if b.startswith("file -r ") or b.startswith("file -rdi "):
                    reference_file = re.findall(r"\"[a-zA-Z]+\"[\s\S]* \"(.+?)\"", b)[0]  # get reference file
                    asset_data = to_kekedou.get_asset_data(reference_file)
                    coco_asset_path = "I:/projects/nzt/to_kekedou/NZT/assets/"
                    coco_asset_path += "{asset_type}/{asset_name}/assembly/{step}/oct/ok/"
                    coco_asset_path = coco_asset_path.format(asset_name=asset_data["asset_name"],
                                                             asset_type=asset_data["asset_type"],
                                                             step=asset_data["step"])

                    coco_asset_f = coco_asset_path + "{asset_name}_rig_oct.ma".format(
                        asset_name=asset_data["asset_name"])

                    b = b.replace(reference_file, coco_asset_f)

                b = b.replace("I:/projects/nzt/to_kekedou", "$SERVER_ROOT")

                f.write(b)

        ver_p = os.path.dirname(ver_file)
        preview_file = glob.glob(ver_p + "/preview/*.mov")
        if preview_file:
            preview_file = preview_file[0]
            # print("preview_file: ", preview_file)
            dst_preview_file = coco_clip_f.replace(".ma", ".mov")
            print("%s =copy=> %s" % (preview_file, dst_preview_file))
            shutil.copy2(preview_file, dst_preview_file)

        action_file = glob.glob(ver_p + "/data/*.ma")
        if action_file:
            action_file = action_file[0]
            # print("action_file: ", action_file)
            dst_action_p = coco_clip_path + "/action"
            if not os.path.isdir(dst_action_p):
                os.makedirs(dst_action_p)
            dst_action_file = dst_action_p + "/" + os.path.basename(ver_file)
            print("%s =copy=> %s" % (action_file, dst_action_file))
            shutil.copy2(action_file, dst_action_file)


if __name__ == '__main__':
    # fix_cam()
    # warriorcrowd_rig_to_kekedou()
    # warriorcrowd_ani_to_kekedou()

    # only_copy_ani_files_wrapper()
    # blocking_to_kekedou()
    # all_to_kekedou_wapper()
    # some_to_kekedou_wapper()
    single_to_kekedou("I:/projects/nzt/shot/i20/i20290/ani/i20290.ani.animation.v003/i20290.ani.animation.v003.ma")
    # json_error_item(save_contains="Success", e=True)
    # json_error_item(save_contains="Success", e=False)
