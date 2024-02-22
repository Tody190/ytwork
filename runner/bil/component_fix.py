# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/28 11:44
"""
import glob

import shotgun_api3

sg = shotgun_api3.Shotgun('http://sg.ds.com/',
                          script_name='Generic',
                          api_key="kalyywr~ayDzxsum3bshirqea")
project_name = "NZT"


if __name__ == '__main__':
    # CustomEntity09
    for p in glob.glob("I:/projects/bil/cache/n10/*/*.*"):
        if not p.endswith(".json"):
            shot_name = p.split("\\")[-2]
            component_name = p.split("\\")[-1]
            filters = [
                ["code", "is", component_name],
                ["sg_entity.Shot.code", "is", shot_name]]
            fields = ["code"]

            component = sg.find("CustomEntity09", filters, fields)
            if component:
                print(shot_name, component_name)
                data = {"code": component[0]["code"].replace(".", ":")}
                sg.update("CustomEntity09", component[0]["id"], data)
