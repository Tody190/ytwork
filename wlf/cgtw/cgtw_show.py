#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 14:55
# @Author  : YangTao
# @File    : cgtw_show.py


import os
import sys
import copy
import traceback

G_base_path = "C:/CgTeamWork_v7/bin/base"

for _path in [
    G_base_path,
    G_base_path + "/com_lib/",
]:
    _path in sys.path or sys.path.append(_path)

from com_api import client_api
from com_widget import widget as ui_widget
from com_widget import dialog as ui_dialog

from com_message_box import message

from PySide2 import QtWidgets
from PySide2 import QtGui

import cgtw2


class Info_Widget(ui_dialog):
    def __init__(self, parent=None):
        super(Info_Widget, self).__init__(parent)
        self.setWindowTitle(u"信息查看器")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), u"view_icon.png")))
        self.main_layout = QtWidgets.QVBoxLayout(self)
        text_browser = QtWidgets.QTextBrowser()
        self.main_layout.addWidget(text_browser)
        self.resize(400, 210)

        t_tw = cgtw2.tw()
        text_browser.append(u"id:            %s" % str(t_tw.client.get_id()))
        text_browser.append(u"database:      %s" % str(t_tw.client.get_database()))
        text_browser.append(u"module:        %s" % str(t_tw.client.get_module()))
        text_browser.append(u"module_type:   %s" % str(t_tw.client.get_module_type()))
        text_browser.append(u"-" * 61)
        text_browser.append(u"link_id:       %s" % str(t_tw.client.get_link_id()))
        text_browser.append(u"link_module:   %s" % str(t_tw.client.get_link_module()))
        text_browser.append(u"filebox_id:    %s" % str(t_tw.client.get_filebox_id()))
        text_browser.append(u"-" * 61)
        text_browser.append(u"event_action:  %s" % str(t_tw.client.get_event_action()))
        text_browser.append(u"event_fields:  %s" % str(t_tw.client.get_event_fields()))
        text_browser.append(u"event_fields:  %s" % str(t_tw.client.get_event_fields()))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Info_Widget()
    win.show()
    sys.exit(app.exec_())
