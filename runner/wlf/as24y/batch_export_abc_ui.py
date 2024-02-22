#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/23 12:28
# @Author  : YangTao
import glob
import os.path
import sys

from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QVBoxLayout
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QLineEdit


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowTitle(u"AS24Y ABC 批量导出")
        self.setGeometry(100, 100, 300, 300)

        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QListWidget.ExtendedSelection)

        self.button = QPushButton(u"确定", )
        self.button.clicked.connect(self.export)
        self.export_path = QLineEdit(u'输入导出路径')

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.export_path)
        self.layout.addWidget(self.button)

        self.setup_data()

    def setup_data(self):
        shot_items = []
        p = '//192.168.1.4/xiangmu/cgteamwork7/AS24Y_STUN/shot_work/animation/*/*/final'
        ani_final_paths = glob.glob(p)
        print(ani_final_paths)
        for ani_f in ani_final_paths:
            ani_f = ani_f.replace('\\', '/')
            shot_name = ani_f.split('/')[9]
            shot_items.append(shot_name)

        self.listWidget.addItems(shot_items)

    def export(self):
        for item in self.listWidget.selectedItems():
            print(item.text())
            print(self.export_path.text())


def showUI():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    showUI()
