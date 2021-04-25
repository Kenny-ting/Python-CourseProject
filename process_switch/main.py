# 七状态模型
import sys
from queue import PriorityQueue
from PyQt5.QtWidgets import *
from window import Mywindow


def main():

    # 创建状态队列
    New = PriorityQueue(maxsize=5)
    Ready = PriorityQueue(maxsize=5)
    Ready_Suspend = PriorityQueue(maxsize=5)
    Running = PriorityQueue(maxsize=1)
    Blocked = PriorityQueue(maxsize=5)
    Blocked_Suspend = PriorityQueue(maxsize=5)
    Exit = PriorityQueue(maxsize=5)
    app = QApplication(sys.argv)
    window = Mywindow(New, Ready, Ready_Suspend, Running, Blocked, Blocked_Suspend, Exit)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
