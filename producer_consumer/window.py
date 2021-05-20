from queue import Queue
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import *
import sys
from semaphore import producer, consumer, P, V
import globalvar as gl
import threading

# 设置全局变量exeContinue
gl._init()
gl.set_value("exeContinue", 0)


class ui_window(object):
    def setupUi(self, MainWindow, Ready, Buffer, Mutex, BufferEmpty, BufferFull):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1650, 1000)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 370, 180, 50))
        self.label.setObjectName("label1")

        self.tableBuffer = QtWidgets.QTableWidget(self.centralwidget)
        self.tableBuffer.setRowCount(1)
        self.tableBuffer.setColumnCount(8)
        self.tableBuffer.verticalHeader().setVisible(False)
        self.tableBuffer.horizontalHeader().setVisible(False)
        self.tableBuffer.setGeometry(QtCore.QRect(350, 350, 805, 100))
        self.tableBuffer.setStyleSheet("background-color:transparent")
        for i in range(8):
            self.tableBuffer.setColumnWidth(i, 100)
            self.tableBuffer.setRowHeight(i, 100)

        self.tableprocess = QtWidgets.QTableWidget(self.centralwidget)
        self.tableprocess.setRowCount(3)
        self.tableprocess.setColumnCount(3)
        self.tableprocess.setVerticalHeaderLabels(['Full', 'Empty', 'Mutex'])
        self.tableprocess.verticalHeader().setStyleSheet("QHeaderView::section "
            "{background-color: transparent; color:black; font:12pt;}")
        self.tableprocess.verticalHeader().setFixedWidth(170)
        self.tableprocess.horizontalHeader().setVisible(False)
        self.tableprocess.setFont(QFont("Times", 15, QFont.Black))
        self.tableprocess.setGeometry(QtCore.QRect(200, 500, 925, 230))
        self.tableprocess.setStyleSheet("background-color:transparent")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(1250, 0, 400, 1000))
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textBrowser.setStyleSheet("background-color:transparent")
        self.textBrowser.setFont(QFont("Times", 12, QFont.Black))
        self.textBrowser.setObjectName("textBrowser")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(200, 750, 900, 150))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_0.setObjectName("pushButton_0")
        self.pushButton_0.clicked.connect(lambda: self.callProducer(Ready, Buffer, BufferEmpty, BufferFull, Mutex))
        self.gridLayout.addWidget(self.pushButton_0, 0, 0, 1, 1)

        self.pushButton_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(lambda: self.callConsumer(Ready, Buffer, BufferEmpty, BufferFull, Mutex))
        self.gridLayout.addWidget(self.pushButton_1, 0, 1, 1, 1)

        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.exeEnd())
        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)

        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda:self.table_fill(Buffer, Mutex, BufferEmpty, BufferFull))
        self.gridLayout.addWidget(self.pushButton_3, 0, 3, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "生产者消费者进程管理"))
        self.label.setFont(QFont("Times", 15, 75))
        self.label.setStyleSheet("color: black")
        self.label.setText(_translate("MainWindow", "Buffer"))
        self.pushButton_0.setText(_translate("MainWindow", "Producer"))
        self.pushButton_1.setText(_translate("MainWindow", "Consumer"))
        self.pushButton_2.setText(_translate("MainWindow", "ExeEnd"))
        self.pushButton_3.setText(_translate("MainWindow", "Show"))

    def callProducer(self, Ready, Buffer, BufferEmpty, BufferFull, Mutex):
        t1 = threading.Thread(target=lambda: producer(Ready, Buffer, BufferEmpty, BufferFull, Mutex), name='t1')
        t1.start()

    def callConsumer(self, Ready, Buffer, BufferEmpty, BufferFull, Mutex):
        t2 = threading.Thread(target=lambda: consumer(Ready, Buffer, BufferEmpty, BufferFull, Mutex), name='t2')
        t2.start()

    def exeEnd(self):
        gl.set_value("exeContinue", 1)

    def set_content(self, myQueue, row):
        temp = Queue(maxsize=3)
        column = 0
        while not myQueue.empty():
            process = myQueue.get()
            # 设置每个位置的文本值
            item = QTableWidgetItem(' %s%s %s' % (process.type, process.id, process.data))
            item.setFont(QFont('Times', 15, QFont.Black))
            # 设置每个位置的文本值
            # 写之前先remove
            self.tableprocess.setItem(row, column, item)
            column += 1
            temp.put(process)
        while not temp.empty():
            process = temp.get()
            myQueue.put(process)

    def set_buffer(self, myQueue):
        temp = Queue(maxsize=8)
        column = 0
        while not myQueue.empty():
            data = myQueue.get()
            # 设置每个位置的文本值
            item = QTableWidgetItem(' %s' %data)
            item.setFont(QFont('Times', 15, QFont.Black))
            # 设置每个位置的文本值
            # 写之前先remove
            self.tableBuffer.setItem(0, column, item)
            column += 1
            temp.put(data)
        while not temp.empty():
            data = temp.get()
            myQueue.put(data)

    def table_fill(self, Buffer, Mutex, BufferEmpty, BufferFull):
        self.tableprocess.clearContents()
        self.tableBuffer.clearContents()
        self.set_buffer(Buffer)

        self.set_content(BufferFull.queue, 0)
        self.set_content(BufferEmpty.queue, 1)
        self.set_content(Mutex.queue, 2)


class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
      self.textWritten.emit(str(text))


class Mywindow(QtWidgets.QWidget, ui_window):
    def __init__(self, Ready, Buffer, Mutex, BufferEmpty, BufferFull):
        super(Mywindow, self).__init__()
        self.setupUi(self, Ready, Buffer, Mutex, BufferEmpty, BufferFull)
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

    def paintEvent(self, event):
        # set background_img
        painter = QPainter(self)
        # rect = QRect(0,0,1000,1200)
        painter.drawRect(self.rect())
        pixmap = QPixmap("./杀猪饲料.jpg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()
