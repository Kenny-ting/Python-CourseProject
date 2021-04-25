from queue import PriorityQueue
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from process import create, admit, dispatch, release, timeout, event_wait, event_occur
from process import ready_activate, ready_suspend, blocked_activate, blocked_suspend, event_occurOutside
from PyQt5.QtGui import *


class ui_window(object):
    def setupUi(self, MainWindow, New, Ready, Ready_Suspend, Running, Blocked, Blocked_Suspend, Exit):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1560, 1000)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap(r"./杀猪饲料.jpg")))
        MainWindow.setPalette(self.palette)
        MainWindow.setAutoFillBackground(True)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 90, 180, 50))
        self.label.setObjectName("label2")

        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setRowCount(7)
        self.table.setColumnCount(5)
        self.table.setVerticalHeaderLabels(['创建', '外存就绪', '外存阻塞',
                                            '内存就绪', '运行', '内存阻塞', '结束'])
        self.table.verticalHeader().setStyleSheet("QHeaderView::section {background-color: transparent}")
        self.table.horizontalHeader().setVisible(False)
        self.table.setFont(QFont("Times", 9, QFont.Black))
        self.table.setGeometry(QtCore.QRect(100, 170, 1394, 527))
        self.table.setStyleSheet("background-color:transparent")
        # 优化1 表格填满窗口
        self.tableView = QTableView()
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(180, 750, 1200, 200))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: create(New, Ready, Ready_Suspend, Running))
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)

        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: admit(New, Ready, Ready_Suspend, Running))
        self.gridLayout.addWidget(self.pushButton_3, 1, 1, 1, 1)

        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(lambda: dispatch(Ready, Running))
        self.gridLayout.addWidget(self.pushButton_5, 1, 2, 1, 1)

        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.clicked.connect(lambda: release(Running, Exit))
        self.gridLayout.addWidget(self.pushButton_9, 1, 4, 1, 1)

        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(lambda: timeout(Ready, Running))
        self.gridLayout.addWidget(self.pushButton_7, 1, 3, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: event_occur(Ready, Blocked))
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)

        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(lambda: event_wait(Running, Blocked))
        self.gridLayout.addWidget(self.pushButton_4, 3, 1, 1, 1)

        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(lambda: ready_activate(Ready, Ready_Suspend))
        self.gridLayout.addWidget(self.pushButton_8, 3, 3, 1, 1)

        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(lambda: ready_suspend(Ready, Ready_Suspend))
        self.gridLayout.addWidget(self.pushButton_6, 3, 2, 1, 1)

        self.pushButton_10 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.clicked.connect(lambda: blocked_activate(Blocked, Blocked_Suspend))
        self.gridLayout.addWidget(self.pushButton_10, 3, 4, 1, 1)

        self.pushButton_11 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_11.clicked.connect(lambda: blocked_suspend(Blocked, Blocked_Suspend))
        self.gridLayout.addWidget(self.pushButton_11, 1, 5, 1, 1)

        self.pushButton_12 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_12.clicked.connect(lambda: event_occurOutside(Ready_Suspend, Blocked_Suspend))
        self.gridLayout.addWidget(self.pushButton_12, 3, 5, 1, 1)

        self.pushButton_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_0.setObjectName("pushButton_0")
        self.pushButton_0.clicked.connect(lambda: self.table_fill(New, Ready, Ready_Suspend, Running, Blocked, Blocked_Suspend, Exit))
        self.gridLayout.addWidget(self.pushButton_0, 0, 2, 1, 2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "七状态模型"))
        self.label.setFont(QFont("Times", 15, QFont.Black))
        self.label.setText(_translate("MainWindow", "状态表"))
        self.pushButton_2.setText(_translate("MainWindow", "创建"))
        self.pushButton_3.setText(_translate("MainWindow", "就绪"))
        self.pushButton_5.setText(_translate("MainWindow", "调度进程"))
        self.pushButton_9.setText(_translate("MainWindow", "释放进程"))
        self.pushButton_7.setText(_translate("MainWindow", "超时"))
        self.pushButton.setText(_translate("MainWindow", "资源到来"))
        self.pushButton_4.setText(_translate("MainWindow", "等待资源"))
        self.pushButton_8.setText(_translate("MainWindow", "激活就绪"))
        self.pushButton_6.setText(_translate("MainWindow", "悬挂就绪"))
        self.pushButton_10.setText(_translate("MainWindow", "激活阻塞"))
        self.pushButton_11.setText(_translate("MainWindow", "悬挂阻塞"))
        self.pushButton_12.setText(_translate("MainWindow", "外存资源"))
        self.pushButton_0.setText(_translate("MainWindow", "展示"))

    def set_content(self, myQueue, row):
        temp = PriorityQueue(maxsize=5)
        column = 0
        while not myQueue.empty():
            process = myQueue.get()
            # 设置每个位置的文本值
            item = QTableWidgetItem(' N:%s  R:%s  S:%d' % (process.name, process.priority, process.memorySize))
            # 设置每个位置的文本值
            # 写之前先remove
            self.table.setItem(row, column, item)
            column += 1
            temp.put(process)
        while not temp.empty():
            process = temp.get()
            myQueue.put(process)

    def table_fill(self, New, Ready, Ready_Suspend, Running, Blocked, Blocked_Suspend, Exit):
        self.table.clearContents ()
        self.set_content(New, 0)
        self.set_content(Ready_Suspend, 1)
        self.set_content(Blocked_Suspend, 2)
        self.set_content(Ready, 3)
        self.set_content(Running, 4)
        self.set_content(Blocked, 5)
        self.set_content(Exit, 6)


class Mywindow(QtWidgets.QWidget, ui_window):
    def __init__(self, New, Ready, Ready_Suspend, Running, Blocked, Blocked_Suspend, Exit):
        super(Mywindow, self).__init__()
        self.setupUi(self, New, Ready, Ready_Suspend, Running, Blocked, Blocked_Suspend, Exit)
