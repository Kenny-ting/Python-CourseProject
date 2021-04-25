import threading


def thread_it(func, *args):
    """将函数放入线程中执行"""
    # 创建线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.setDaemon(True)
    # 启动线程
    t.start()