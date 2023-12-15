# coding:utf-8
import pprint
import sys
import os
import traceback
import copy

CGTW_ROOT_BIN = __file__.replace(u"\\", u"/").split(u"ext_plugin")[0]
#plugin_file = u"C:/CgTeamWork_v6.2/bin/CGTW_Bat_Publish/cgtw_bat_publish.py"
#CGTW_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(plugin_file)))  # C:/CgTeamWork_v6.2
for _path in [
    CGTW_ROOT_BIN + u"base",
    CGTW_ROOT_BIN + u"lib/pyside",
    CGTW_ROOT_BIN + u"cgtw",
    CGTW_ROOT_BIN + u"base/com_lib",
    CGTW_ROOT_BIN + u"base/com_icon"
]:
    print(_path)
    _path in sys.path or sys.path.append(_path)

# pyside
from PySide2 import QtWidgets
from PySide2 import QtGui
QtWidgets.QApplication.addLibraryPath(CGTW_ROOT_BIN + "lib/pyside/PySide2/plugins/")

# cgtw
import cgtw2


class Info_Widget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Info_Widget, self).__init__(parent)
        self.setWindowTitle(u"信息查看器")
        print(os.path.join(os.path.dirname(__file__), u"view_icon.png"))
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
    try:
        app = QtWidgets.QApplication(sys.argv)
        info_widget = Info_Widget()
        info_widget.show()
        app.exec_()
    except Exception as e:
        import os
        print(traceback.format_exc())
