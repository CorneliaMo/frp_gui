# coding=utf-8

import sys
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidget, QAbstractItemView, QPushButton, QLabel, \
    QFrame, QTableWidgetItem, QDialog
import json


class newWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    x_size = 470
    y_size = 300

    def initUI(self):
        self.setWindowTitle('新建代理')
        self.resize(self.x_size, self.y_size)
        self.show()


class FatherWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    x_size = 470
    y_size = 300

    def newWin(self):
        childwindow = newWindow()
        childwindow.show()
        childwindow.exec_()

    def switch(self):
        if self.status:
            self.boot_button.setText("启动")
            self.status_label.setText(self.off)
            self.status = False
        else:
            self.boot_button.setText("关闭")
            self.status_label.setText(self.on)
            self.status = True

    def initUI(self):
        self.setGeometry(960 - self.x_size // 2, 540 - self.y_size // 2, self.x_size, self.y_size)
        self.setWindowTitle("frp_gui")
        self.loadList()
        self.initTable()
        self.fillTable()
        self.statusFlags()

    def loadList(self):
        # 加载已存在的映射列表
        with open("frp.json", mode='r') as fp:
            self.frp_list = json.load(fp)

    def initTable(self):
        # 端口映射列表
        self.table = QTableWidget(1, 5, self)
        self.table.resize(450, 245)
        self.table.move(10, 45)
        self.table.setFrameShape(QFrame.NoFrame)  # 设置无表格的外框
        self.table.setRowCount(300)
        self.table.setHorizontalHeaderLabels(["名称", "类型", "本地端口", "远程端口", "本地地址"])
        self.table.horizontalHeader().setStretchLastSection(True)  # 设置最后一列拉伸至最大
        self.table.horizontalHeader().setFixedHeight(20)  # 设置表头高度
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeRowsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 只读不可修改
        self.table.horizontalHeader().resizeSection(0, 100)
        self.table.horizontalHeader().resizeSection(1, 60)
        self.table.horizontalHeader().resizeSection(2, 60)
        self.table.horizontalHeader().resizeSection(3, 60)
        self.table.horizontalHeader().resizeSection(4, 60)

    def fillTable(self):
        for i in range(len(self.frp_list)):
            item0 = QTableWidgetItem(self.frp_list[i]["name"])
            item0.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, item0)
            item1 = QTableWidgetItem(self.frp_list[i]["type"])
            item1.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, item1)
            item2 = QTableWidgetItem(str(self.frp_list[i]["localPort"]))
            item2.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 2, item2)
            item3 = QTableWidgetItem(str(self.frp_list[i]["remotePort"]))
            item3.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, item3)
            item4 = QTableWidgetItem(self.frp_list[i]["localIP"])
            item4.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 4, item4)

    def statusFlags(self):
        self.status = False
        # frpc客户端状态
        status_lable = QLabel(self)
        status_lable.setText("frpc状态：")
        status_lable.move(120, 10)

        # 状态指示
        self.off = "<font color=red>关闭</font>"
        self.on = "<font color=green>开启</font>"
        self.status_label = QLabel(self)
        self.status_label.setText(self.off)
        self.status_label.move(180, 10)

        # 启动/关闭frpc客户端按钮
        self.boot_button = QPushButton(self)
        self.boot_button.setText("启动")
        self.boot_button.move(10, 10)
        self.boot_button.clicked.connect(self.switch)

        # 新建代理
        new_button = QPushButton(self)
        new_button.setText("新建穿透")
        new_button.move(215, 10)
        new_button.clicked.connect(self.newWin)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建app
    win = FatherWindow()
    win.show()
    sys.exit(app.exec_())
