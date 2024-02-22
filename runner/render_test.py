# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/4 20:40
"""
import sys

path = "D:/yangtao/work/packages/studio/oct_cache_exporter/dev/python"
path in sys.path or sys.path.append(path)

from oct_cache_exporter import submitter


def submit_to_local(version_id):
    vs = submitter.VersionSubmiter(version_id=version_id)
    vs.executable = "rez-env.exe"
    vs.executable_arguments = "oct_maya-dev maya-2019 maya_plugins oct_cache_exporter-dev -- export_cache"
    vs.submit_to_local()


def submit_to_deadline(version_id):
    vs = submitter.VersionSubmiter(version_id=version_id)
    vs.submit_to_deadline()


submit_to_local("207685")
