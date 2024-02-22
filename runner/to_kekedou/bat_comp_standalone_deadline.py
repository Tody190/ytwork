# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/14 18:04
"""


import json
import glob
import math
import os
import sys

DEADLINE_REPOSITORY_ROOT = '//192.168.15.15/DeadlineRepository10'
DEADLINE_WEBSERVICE_PORT = 8082
DEADLINE_WEBSERVICE_HOST = '192.168.15.15'

sys.path.append('{0}/api/python'.format(DEADLINE_REPOSITORY_ROOT))
import Deadline.DeadlineConnect as Connect
import getpass

USER = getpass.getuser()

client = Connect.DeadlineCon(DEADLINE_WEBSERVICE_HOST, DEADLINE_WEBSERVICE_PORT)

def to_deadline(ma_file):
    version_name = os.path.basename(ma_file)
    JobInfo = {
        'Name': '%s' % version_name,
        'Plugin': 'CommandLine',
        'BatchName': 'batch_shot_comp',
        'UserName': USER,
        'EnvironmentKeyValue0': 'MA_FILE=%s' % ma_file,
    }
    PluginInfo = {
        'Executable': 'rez-env.exe',
        'Arguments': "oct_maya maya-2019 maya_plugins -- mayapy W:/projects/nzt/misc/users/yangtao/main_code/runner/to_kekedou/bat_comp_standalone.py"
    }

    new_job = client.Jobs.SubmitJob(JobInfo, PluginInfo)

    # new_job["Props"]["Env"]["JOBID"] = new_job['_id']
    # client.Jobs.SaveJob(new_job)

if __name__ == '__main__':
    ma_file = "I:/projects/nzt/shot/i20/i20370/ani/i20370.ani.animation/i20370.ani.animation.v002.ma"
    to_deadline(ma_file)