from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time

global img
global im_root
global img_bar
global img_bar_root


def bar_figure(word_data):
    # 将全局的字体设置为黑体
    matplotlib.rcParams['font.family'] = 'SimHei'

    # 数据
    num = 12
    x = np.arange(num)
    y = []
    for index, word in enumerate(word_data):
        if index < 12:
            y.append(word[1])

    # 添加横轴坐标名称
    x_name = (word_data[0][0], word_data[1][0], word_data[2][0], word_data[3][0],
              word_data[4][0], word_data[5][0], word_data[6][0], word_data[7][0],
              word_data[8][0], word_data[9][0], word_data[10][0], word_data[11][0])

    # 绘图 x x轴， height 高度, width=0.8
    p1 = plt.bar(x, height=y, width=0.5, color='SkyBlue', label="热词词频", tick_label=x_name)

    # 添加数据标签
    for a, b in zip(x, y):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)

    # 添加图例
    plt.legend()

    # 展示图形
    plt.savefig('C:/Users/ljt0/PycharmProjects/news_word_analysis/bar.png')
    time.sleep(2)


def show_data(word_data, news_type):  # 显示数据
    global img
    global im_root
    root1 = Tk()  # 副窗口
    root1.geometry('900x562')  # 修改窗口大小
    root1.title(news_type + ' 新闻板块')  # 副窗口标题

    img = Image.open('one_piece.png').resize((900, 562))
    im_root = ImageTk.PhotoImage(img)  # 做全局变量

    background = Label(root1, image=im_root)
    background.pack(fill=BOTH, expand=YES)

    # 设置文本框
    group = LabelFrame(root1, padx=0, pady=0)  # 框架
    group.place(x=100, y=195)

    word_str = ""
    for index, word in enumerate(word_data):
        if index < 12:
            if index % 2 == 0:
                # 每两个热词组成一个label标签，作为一行
                word_str = ""   # 清空，准备下一行标签的内容
                word_str += word[0] + ': ' + str(word[1]) + '\t'

            if index % 2 == 1:  # 没两组输出一次
                word_str += word[0] + ': ' + str(word[1])
                print(word_str)
                w = Label(group, text=word_str, font=("微软雅黑", 12))
                w.pack(anchor=W)

    Label(root1, text=news_type + ' 新闻板块热词', font=("微软雅黑", 18)).place(x=315, y=50, height=50)  # 温馨提示

    Label(root1, text="Author: Kenny_ting", fg="black", bg="yellow").place(x=100, y=480)

    global img_bar
    global img_bar_root
    bar_figure(word_data)
    img_bar = Image.open('bar.png').resize((480, 300))
    img_bar_root = ImageTk.PhotoImage(img_bar)  # 做全局变量
    Label(root1, image=img_bar_root).place(x=330, y=145, width=480, height=300)

    Button(root1, text='确认并退出', width=10, command=root1.quit).place(x=700, y=480, width=80, height=40)  # 退出按钮

    root1.mainloop()
