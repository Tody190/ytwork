#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/29 13:57
# @Author  : YangTao

import os
import glob
import json
import pprint


def go():
    p = 'Z:/cgteamwork7/AS24Y_STUN/shot_work/check_render/*/*/abc/*.wsd'
    ani_final_path = glob.glob(p)
    for wsd_f in ani_final_path:

        with open(wsd_f, 'r') as f:
            data = json.load(f)
            eles = data['SceneElements']

            for e in eles:
                root_list = []
                if isinstance(e['ERoot'], list):
                    root_list = e['ERoot']
                else:
                    root_list.append(e['ERoot'])

                maya_file_name = os.path.basename(e['EPath']).rsplit('.', 1)[0]
                maya_file_name = maya_file_name.replace('FX.', '')

                _maya_file_name = maya_file_name.replace('_lo', '')
                _maya_file_name = _maya_file_name.replace('_hi', '')

                maya_ns_name = root_list[0].split('|')[-1].split(':')[0]

                _maya_ns_name = maya_ns_name.replace('_hi', '')
                _maya_ns_name = _maya_ns_name.replace('_lo', '')

                if _maya_file_name != _maya_ns_name:
                    print(os.path.basename(wsd_f).replace('.wsd', ''))
                    print('maya_ns: ', maya_ns_name)
                    print('file_name: ', maya_file_name)
                    print('\n')


if __name__ == '__main__':
    go()