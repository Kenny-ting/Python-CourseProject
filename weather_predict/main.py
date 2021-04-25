# python实验一
# 查询某一城市的天气

from tkinter import *
from thread_it import thread_it
from get_weather_data import get_weather_day

global root


def win_quit():
    global root
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.destroy()


def main():
    # 输入窗口
    global root
    root = Tk()
    root.title('天气查询')  # 窗口标题
    Label(root, text='请输入城市').grid(row=0, column=0)  # 设置标签并调整位置
    enter = Entry(root)  # 输入框
    enter.grid(row=0, column=1, padx=20, pady=20)  # 调整位置
    enter.delete(0, END)  # 清空输入框
    enter.insert(0, '沈阳')  # 设置默认文本
    enter_text = enter.get()  # 获取输入框的内容

    # 布置按键
    Button(root, text="确认", width=10, command=lambda: win_quit()) \
        .grid(row=3, column=1, sticky=E, padx=10, pady=5)
    # lambda: thread_it(get_weather_day, enter_text)

    root.mainloop()  # the main thread

    get_weather_day(enter_text)


if __name__ == '__main__':
    main()
