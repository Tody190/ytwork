# coding:utf-8
import pprint
import sys
import os
import traceback
import copy

#CGTW_ROOT_BIN = __file__.replace(u"\\", u"/").split(u"ext_plugin")[0]
#plugin_file = u"C:/CgTeamWork_v6.2/bin/CGTW_Bat_Publish/cgtw_bat_publish.py"
#CGTW_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(plugin_file)))  # C:/CgTeamWork_v6.2

CGTW_ROOT_BIN = "C:/CgTeamWork_v7/bin"
for _path in [
    CGTW_ROOT_BIN + u"base",
    CGTW_ROOT_BIN + u"lib/pyside",
    CGTW_ROOT_BIN + u"cgtw",
    CGTW_ROOT_BIN + u"base/com_lib",
    CGTW_ROOT_BIN + u"base/com_icon"
]:
    print(_path)
    _path in sys.path or sys.path.append(_path)

# # pyside
# from PySide2 import QtWidgets
# from PySide2 import QtGui
# QtWidgets.QApplication.addLibraryPath(CGTW_ROOT_BIN + "lib/py2/pyside/PySide2/plugins/")

# cgtw
import cgtw2

t_tw = cgtw2.tw()
print(u"id:            %s" % str(t_tw.client.get_id()))
print(u"database:      %s" % str(t_tw.client.get_database()))
print(u"module:        %s" % str(t_tw.client.get_module()))
print(u"module_type:   %s" % str(t_tw.client.get_module_type()))
print(u"-" * 61)
print(u"link_id:       %s" % str(t_tw.client.get_link_id()))
print(u"link_module:   %s" % str(t_tw.client.get_link_module()))
print(u"filebox_id:    %s" % str(t_tw.client.get_filebox_id()))
print(u"-" * 61)
print(u"event_action:  %s" % str(t_tw.client.get_event_action()))
print(u"event_fields:  %s" % str(t_tw.client.get_event_fields()))
print(u"event_fields:  %s" % str(t_tw.client.get_event_fields()))

import time
time.sleep(600)

# t_dict = {"module": "task",
#           "module_type": "task",
#           "db": "proj_text_cg_v04",
#           "task_id": t_id,
#           "filebox_data": t_filebox_data,
#           "file_path_list": t_upload_list,
#           'des_file_path_list': t_online_list,
#           'version': t_version}
#
# t_tw.send_local_http("proj_text_cg_v04",
#                      "shot",
#                      u"filebox_bulk_upload_to_filebox",
#                      u"get")
