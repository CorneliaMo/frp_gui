# coding=utf-8

from json import load, dump
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QAbstractItemView, QPushButton, QLabel, \
    QFrame, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, QComboBox

import booter
import generator


class newWindow(QDialog):
    def __init__(self, origin):
        super().__init__()
        self.origin = origin
        self.initUI()

    x_size = 200
    y_size = 100

    def initUI(self):
        self.setWindowTitle('add config')
        self.resize(self.x_size, self.y_size)
        self.setText()

    def commit(self):
        # 加载已存在的映射列表
        with open("frp.json", mode='r') as fp:
            frp_list = load(fp)
        with open("frp.json", mode='w') as fp:
            frp_list.append({"name": self.name_input.text(), "type": self.type_input.currentText(),
                             "localIP": self.localIP_input.text(), "localPort": int(self.localPort_input.text()),
                             "remotePort": int(self.remoteIP_input.text())})
            dump(frp_list, fp)
        self.close()
        self.origin.loadList()
        self.origin.fillTable()

    def setText(self):
        layout = QVBoxLayout()
        name_label = QLabel(self)
        name_label.setText("名称")
        layout.addWidget(name_label)
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_input)
        type_label = QLabel(self)
        type_label.setText("类型")
        layout.addWidget(type_label)
        self.type_input = QComboBox(self)
        self.type_input.addItem("tcp")
        self.type_input.addItem("udp")
        layout.addWidget(self.type_input)
        localIP_label = QLabel(self)
        localIP_label.setText("本地地址")
        layout.addWidget(localIP_label)
        self.localIP_input = QLineEdit(self)
        self.localIP_input.setText("127.0.0.1")
        layout.addWidget(self.localIP_input)
        localPort_label = QLabel(self)
        localPort_label.setText("本地端口")
        layout.addWidget(localPort_label)
        self.localPort_input = QLineEdit(self)
        layout.addWidget(self.localPort_input)
        remoteIP_label = QLabel(self)
        remoteIP_label.setText("远程端口")
        layout.addWidget(remoteIP_label)
        self.remoteIP_input = QLineEdit(self)
        layout.addWidget(self.remoteIP_input)
        commit_button = QPushButton("")
        commit_button.setText("提交")
        commit_button.clicked.connect(self.commit)
        layout.addWidget(commit_button)
        self.setLayout(layout)


class editWindow(newWindow):
    def __init__(self, origin, row):
        super().__init__(origin)
        self.row = row
        self.fillText()

    def commit(self):
        # 加载已存在的映射列表
        with open("frp.json", mode='r') as fp:
            frp_list = load(fp)
        with open("frp.json", mode='w') as fp:
            frp_list[self.row] = {"name": self.name_input.text(), "type": self.type_input.currentText(),
                                  "localIP": self.localIP_input.text(), "localPort": int(self.localPort_input.text()),
                                  "remotePort": int(self.remoteIP_input.text())}
            dump(frp_list, fp)
        self.close()
        self.origin.loadList()
        self.origin.fillTable()

    def fillText(self):
        self.name_input.setText(self.origin.table.item(self.row, 0).text())
        self.localIP_input.setText(self.origin.table.item(self.row, 4).text())
        self.localPort_input.setText(self.origin.table.item(self.row, 2).text())
        self.remoteIP_input.setText(self.origin.table.item(self.row, 3).text())
        type = self.origin.table.item(self.row, 1).text()
        if type == "tcp":
            self.type_input.setCurrentIndex(0)
        elif type == "udp":
            self.type_input.setCurrentIndex(1)


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.frpClient = booter.frpcBooter()
        self.initUI()

    x_size = 470
    y_size = 300

    def newWin(self):
        childwindow = newWindow(self)
        childwindow.show()
        childwindow.exec_()

    def switch(self):
        if self.status:
            self.boot_button.setText("启动")
            self.status_label.setText(self.off)
            self.status = False
            print(self.frpClient.status())
            if self.frpClient.status():
                self.frpClient.shutup()
        else:
            self.boot_button.setText("关闭")
            self.status_label.setText(self.on)
            self.status = True
            generator.generator()
            self.frpClient.startup()

    def initUI(self):
        self.setGeometry(960 - self.x_size // 2, 540 - self.y_size // 2, self.x_size, self.y_size)
        self.setWindowTitle("frp_gui")
        self.loadList()
        self.initTable()
        self.fillTable()
        self.statusFlags()

    def newEdit(self, item):
        childwindow = editWindow(self, item.row())
        childwindow.show()
        childwindow.exec_()

    def loadList(self):
        # 加载已存在的映射列表
        with open("frp.json", mode='r') as fp:
            self.frp_list = load(fp)

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
        self.table.itemDoubleClicked.connect(self.newEdit)

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

    def reloadTable(self):
        for i in range(len(self.frp_list)):
            self.table.removeRow(0)
        self.loadList()
        self.fillTable()

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

        # 删除代理
        del_button = QPushButton(self)
        del_button.setText("删除穿透")
        del_button.move(320, 10)
        del_button.clicked.connect(self.delete)

    def delete(self):
        if self.table.selectedItems():
            try:
                # 加载已存在的映射列表
                with open("frp.json", mode='r') as fp:
                    frp_list = load(fp)
                with open("frp.json", mode='w') as fp:
                    del frp_list[self.table.selectedItems()[0].row()]
                    dump(frp_list, fp)
                self.reloadTable()
            except:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建app
    win = mainWindow()
    win.show()
    sys.exit(app.exec_())
