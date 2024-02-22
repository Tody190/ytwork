# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/31 19:55
"""
import json
import os
from datetime import datetime
import pprint
import unicodedata

import project_files

target_date = datetime(2023, 9, 1)
shots = ["i10", "i20", "n80", "n90", "m90"]
json_file = "W:/projects/nzt/misc/users/yangtao/output/i10i20n80n90m90_creation_time.json"
text_file = "W:/projects/nzt/misc/users/yangtao/output/i10i20n80n90m90_time.txt"


def get_time_shot_files():
    shots_files = {}
    for s in shots:
        max_files = project_files.get_w_files("nzt", s, ["ani", "lay"])
        for shot_name, files_list in max_files.items():
            print(shot_name)
            for f in files_list:
                creation_time = datetime.fromtimestamp(os.path.getctime(f))
                if creation_time < target_date:
                    time_str = creation_time.strftime("%Y-%m-%d %H:%M:%S")
                    kkd_shot_name = project_files.get_kekedou_shot_name(shot_name)
                    if kkd_shot_name:
                        if kkd_shot_name in shots_files.keys():
                            shots_files[kkd_shot_name].append((os.path.basename(f), time_str))
                        else:
                            shots_files[kkd_shot_name] = [(os.path.basename(f), time_str)]
    return shots_files


# format data
def write_data():
    format_data = {}
    shots_fs = get_time_shot_files()
    txt_info = ""
    for shot_name, files_data in shots_fs.items():
        if shot_name and files_data:
            txt_info += str(shot_name) + "," + str(len(files_data)) + ","
            files_creation_time_map = {}
            files_data = sorted(files_data, key=lambda x: x[-1], reverse=True)
            for f, time_str in files_data:
                if len(f) > 35:
                    print(f)
                    continue

                txt_info += str(f) + ":  (" + time_str + ")    "
                files_creation_time_map[str(f)] = str(time_str)

            txt_info += "\n"

            format_data[shot_name] = {"files_count": len(files_data),
                                      "files_creation_time": files_creation_time_map}

    with open(json_file, 'w') as f:
        pprint.pprint(format_data)
        json.dump(format_data, f, indent=4, ensure_ascii=False, sort_keys=True)

    with open(text_file, 'w') as f:
        f.write(txt_info)


write_data()

# format_data = {"xxx": "dddddsf年号"}
#
# with open(json_file, 'w') as f:
#     pprint.pprint(format_data)
#     json.dump(format_data, f, indent=4, ensure_ascii=True, sort_keys=True)