from queue import Queue
import globalvar as gl
import time
# 定义编号
pid = 1
cid = 1
data = 1


# 定义信号量类
class Semaphore:
    count = 0
    name = None
    queue = None

    def __init__(self, num, sname):  # 初始化信号量的定义
        self.count = num
        self.name = sname
        self.queue = Queue(maxsize=0)


# 定义进程类
class Process:
    # 定义基本属性
    id = 0      # 进程id
    type = 'P'  # 标识是生产者进程还是消费者进程
    data = 0    #

    def __init__(self, type, id, data):  # 初始化进程的定义
        self.type = type
        self.id = id
        self.data = data


def printLog(Ready, BufferEmpty, BufferFull, Mutex, Process):
    print("==========")
    print("BufferEmpty: {}".format(BufferEmpty.count))
    print("BufferFull: {}".format(BufferFull.count))
    print("Mutex: {}".format(Mutex.count))
    print("Current: ", end="")
    if Process.type == 'P':
        print("P{}".format(Process.id))
    elif Process.type == 'C':
        print("C{}".format(Process.id))
    if not Ready.empty():
        process = Ready.get()
        print("Ready: %s%s" %(process.type, process.id))
        Ready.put(process)
    else:
        print("Ready: None")


def P(s, process):
    """
    This is the function P to call when the process uses resources
    :param s: 信号量
    :param process: 进程
    :return: True when process is suspended
    """
    # s 计数减 1
    s.count = s.count - 1
    if s.count < 0:
        # 如果 s.count < 0 调用进程进入等待队列阻塞该进程
        s.queue.put(process)
        return True
    else:
        return False


def V(s, Ready, Buffer, BufferEmpty, BufferFull, Mutex):
    """
    This is the function V to call when the process has already used resources
    :param s: 信号量
    :param process: 进程
    :return:
    """
    # s 计数减 1
    s.count = s.count + 1
    if s.count <= 0:
        # 如果 s.count <= 0 说明此时有阻塞进程
        process = s.queue.get()
        # 放到 Ready 中
        Ready.put(process)
        if process.type == 'P':
            time.sleep(5)
            if s.name != "Mutex":
                P(Mutex, process)
            printLog(Ready, BufferEmpty, BufferFull, Mutex, process)
            while True:
                if gl.get_value("exeContinue") == 1:
                    # 放数据并执行取操作
                    Buffer.put(process.data)
                    V(Mutex, Ready, Buffer, BufferEmpty, BufferFull, Mutex)
                    V(BufferFull, Ready, Buffer, BufferEmpty, BufferFull, Mutex)
                    gl.set_value("exeContinue", 0)
                    break
            Ready.get()

        elif process.type == 'C':
            time.sleep(5)
            if s.name != "Mutex":
                P(Mutex, process)
            printLog(Ready, BufferEmpty, BufferFull, Mutex, process)
            while True:
                if gl.get_value("exeContinue") == 1:
                    # 放数据并执行取操作
                    process.data = Buffer.get()
                    # print("%s" % process.data)
                    V(Mutex, Ready, Buffer, BufferEmpty, BufferFull, Mutex)
                    V(BufferEmpty, Ready, Buffer, BufferEmpty, BufferFull, Mutex)
                    gl.set_value("exeContinue", 0)
                    break
            Ready.get()


def producer(Ready, Buffer, BufferEmpty, BufferFull, Mutex):
    """
    创建生产者进程
    :return: None
    """
    global pid, data

    if Ready.empty():
        # 创建producer进程
        process = Process('P', pid, data)
        pid = pid + 1
        data = data + 1
    else:
        process = Ready.get()
    # 操作
    if not P(BufferEmpty, process):
        if not P(Mutex, process):
            printLog(Ready, BufferEmpty, BufferFull, Mutex, process)
            while True:
                if gl.get_value("exeContinue") == 1:
                    # 放数据并执行取操作
                    Buffer.put(process.data)
                    V(Mutex, Ready, Buffer, BufferEmpty, BufferFull, Mutex)
                    V(BufferFull, Ready, Buffer, BufferEmpty, BufferFull, Mutex)
                    gl.set_value("exeContinue", 0)
                    break

    printLog(Ready, BufferEmpty, BufferFull, Mutex, process)


def consumer(Ready, Buffer, BufferEmpty, BufferFull, Mutex):
    """
    创建消费者进程
    :return: None
    """
    global cid
    if Ready.empty():
        # 创建consumer进程
        process = Process('C', cid, 0)
        cid = cid + 1
    else:
        process = Ready.get()
    # 操作
    if not P(BufferFull, process):
        if not P(Mutex, process):
            printLog(Ready, BufferEmpty, BufferFull, Mutex, process)
            while True:
                if gl.get_value("exeContinue") == 1:
                    # 放数据并执行取操作
                    process.data = Buffer.get()
                    # print("%s" % process.data)
                    V(Mutex, Ready, Buffer, BufferEmpty, BufferFull, Mutex)
                    V(BufferEmpty, Ready, Buffer, BufferEmpty, BufferFull, Mutex)
                    gl.set_value("exeContinue", 0)
                    break

    printLog(Ready, BufferEmpty, BufferFull, Mutex, process)
