# 状态定义
import random
import operator
import time

# 定义初始变量
pid = int(random.random() * 10000)  # 随机生成一个进程号
name = ord('a') - 1  # 第一个进程名是‘a’
MaxSize = 100  # 内存最大空间100M
rank = {1: "low-level", 2: "mid-level", 3: "important"}


# 定义进程
class Process:
    # 定义基本属性
    name = ''  # 进程名
    pid = 0  # 进程id
    memorySize = 0  # 内存空间大小
    priority = 0  # 优先级

    def __init__(self, n, pid, m, p):  # 初始化进程的定义
        self.name = n
        self.pid = pid
        self.memorySize = m
        self.priority = p

    def __lt__(self, other):  # 定义优先级别
        # python3 中已经启用cmp函数,__cmp__方法也弃用了
        # 你只需要实现 __lt__ 方法和其他任意一个方法就可以了.
        return operator.lt(self.priority, other.priority)


# 随机分配合适大小的内存函数
def allocate_memory():
    size = int(random.randrange(1, 50))  # 生成一个大小适中的size
    return size


# 随机设置优先级的函数
def set_priority():
    pri = int(random.randrange(1, 4))  # 生成一个大小适中的size
    return pri


# 创建进程函数
def create(New, Ready, Ready_Suspend, Running):
    global name, pid, MaxSize  # 使用初始变量定义进程

    # 如果创建队列未满
    if New.full() == 0:
        name += 1
        size = allocate_memory()
        pri = set_priority()

        # 生成进程，并插入创建队列
        temp = Process(chr(name), pid + 1, size, pri)
        New.put(temp)
        print("创建进程成功！")

        # 调用admit()函数
        admit(New, Ready, Ready_Suspend, Running)
        return True
    # 创建队列满了
    else:
        print("创建队列满！请等待！")
        return False


# 进程允许进入内存
def admit(New, Ready, Ready_Suspend, Running):
    global MaxSize

    # 如果就绪队列未满
    if Ready.full() == 0:
        temp = New.get()
        size = temp.memorySize
        if size < MaxSize:
            # 从创建队列中取出，进入内存
            Ready.put(temp)
            MaxSize -= size
            print("进程{}已就绪!剩余内存大小：".format(temp.name), MaxSize)
        else:
            print("内存已满！")
            # 内存不足，放到外存中
            if not Ready_Suspend.full():
                Ready_Suspend.put(temp)
            else:
                # 外存也满了，就不动了
                New.put(temp)

    # 就绪队列已满
    else:
        print("Please wait! The Ready queue is full!...")
        return False

    dispatch(Ready, Running)
    return True


# 分配进程,分配成功返回值为真，否则为0
def dispatch(Ready, Running):
    # 如果当前运行态为空，则需要调度
    if Running.empty():
        # 从就绪队列中取出一个优先级高的进程
        process = Ready.get()
        Running.put(process)
        print("进程{}调度成功！".format(process.name))
        print("============")
        return True
    else:
        if Ready.empty():
            print("没有可以调度的进程！")
        else:
            print("已有进程正在运行")
        print("============")
        return False


# 释放进程
def release(Running, Exit):
    global MaxSize

    if not Running.empty():
        # 释放当前正在运行的进程
        process = Running.get()
        MaxSize += process.memorySize
        Exit.put(process)
        print("进程{}已释放!剩余内存大小：".format(process.name), MaxSize)
        return True
    else:
        print("没有正在运行的进程！")
        return False


# 超时了
def timeout(Ready, Running):
    if not Running.empty():
        # 当前正在运行的进程超时
        process = Running.get()
        Ready.put(process)
        print("进程{}已超时!".format(process.name))
        return True
    else:
        print("没有正在运行的进程！")
        return False


# 等待资源
def event_wait(Running, Blocked):
    if not Running.empty():
        # 阻塞当前正在运行的进程
        process = Running.get()
        Blocked.put(process)
        print("进程{}被阻塞!".format(process.name))
        return True
    else:
        print("没有正在运行的进程！")
        return False


# 资源就位
def event_occur(Ready, Blocked):
    if not Ready.full() and not Blocked.empty():
        process = Blocked.get()
        Ready.put(process)
        print("进程{}已就绪!".format(process.name))
    else:
        print("阻塞队列为空！没有等待资源的进程！")


def ready_activate(Ready, Ready_Suspend):
    global MaxSize

    if not Ready_Suspend.empty():
        process = Ready_Suspend.get()
        size = process.memorySize
        if size < MaxSize and not Ready.full():
            Ready.put(process)
            MaxSize -= size
            print("外存进程{}已就绪!剩余内存大小：".format(process.name), MaxSize)
        else:
            Ready_Suspend.put(process)
            print("激活 外存就绪进程失败！")
    return False


def ready_suspend(Ready, Ready_Suspend):
    global MaxSize
    if not Ready.empty() and not Ready_Suspend.full():
        process = Ready.get()
        size = process.memorySize
        Ready_Suspend.put(process)
        MaxSize += size
        print("内存进程{}被悬挂!剩余内存大小：".format(process.name), MaxSize)
    else:
        print("悬挂 内存就绪进程失败！")
    return False


def blocked_activate(Blocked, Blocked_Suspend):
    global MaxSize

    if not Blocked_Suspend.empty():
        process = Blocked_Suspend.get()
        size = process.memorySize
        if size < MaxSize and not Blocked.full():
            Blocked.put(process)
            MaxSize -= size
            print("外存阻塞进程{}已激活!剩余内存大小：".format(process.name), MaxSize)
        else:
            Blocked_Suspend.put(process)
            print("激活 外存阻塞进程失败！")
    return False


def blocked_suspend(Blocked, Blocked_Suspend):
    global MaxSize
    if not Blocked.empty() and not Blocked_Suspend.full():
        process = Blocked.get()
        size = process.memorySize
        Blocked_Suspend.put(process)
        MaxSize += size
        print("内存阻塞进程{}被悬挂!剩余内存大小：".format(process.name), MaxSize)
    else:
        print("悬挂 阻塞进程失败！")
    return False


def event_occurOutside(Ready_Suspend, Blocked_Suspend):
    if not Ready_Suspend.full() and not Blocked_Suspend.empty():
        process = Blocked_Suspend.get()
        Ready_Suspend.put(process)
        print("外存阻塞进程{}在外存就绪!".format(process.name))
    else:
        print("外存阻塞进程就绪失败！")