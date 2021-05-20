# 生产者消费者进程管理
import sys
from PyQt5.QtWidgets import *
from window import Mywindow
from queue import Queue
from semaphore import Semaphore


def main():

    Ready = Queue(maxsize=1)    # 当前就绪进程
    Buffer = Queue(maxsize=8)   # 定义缓冲区
    Mutex = Semaphore(1, "Mutex")        # 互斥信号量
    BufferEmpty = Semaphore(8, "BufferEmpty")  # Empty信号量
    BufferFull = Semaphore(0, "BufferFull")   # Full 信号量

    app = QApplication(sys.argv)
    window = Mywindow(Ready, Buffer, Mutex, BufferEmpty, BufferFull)
    window.paintEngine()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

