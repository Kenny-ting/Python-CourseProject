from tkinter import *

import matplotlib
from PIL import Image, ImageTk
import re
import matplotlib.pyplot as plt

global img
global im_root


def draw_line_chart(weather_dict):
    # 将全局的字体设置为黑体
    matplotlib.rcParams['font.family'] = 'SimHei'

    y_high = []
    y_low = []
    x_date = []
    x = list(range(7))

    for i in range(7):  # 将每一天的数据放入列表中
        y_high.append(weather_dict[i].get('最高气温'))
        y_low.append(weather_dict[i].get('最低气温'))
        pattern = re.compile(r'\((.*)\)')
        x_date.append(pattern.findall(weather_dict[i].get('日期'))[0])

    plt.plot(x, y_low, 'b*-', label="low")   # 画出最低气温
    plt.plot(x, y_high, 'ro-', label="high")  # 画出最高气温

    labels = tuple(x_date)
    plt.xticks(x, labels)  # 给出横轴标签

    # 添加图例、标题
    plt.legend()
    plt.title("最高温与最低温变化折线图")

    plt.savefig('C:/Users/ljt0/PycharmProjects/pythonProject/line_chart.png')
    plt.show()


def show_data(weather_dict, city_name):  # 显示数据

    global img
    global im_root
    root1 = Tk()  # 副窗口
    root1.geometry('890x390')  # 修改窗口大小
    root1.title(city_name + '天气状况')  # 副窗口标题

    img = Image.open('canvs.png').resize((890, 390))  # canvas.jpg
    im_root = ImageTk.PhotoImage(img)  # 做全局变量

    background = Label(root1, image=im_root)
    background.pack(fill=BOTH, expand=YES)

    # 设置日期列表
    for i in range(7):  # 将每一天的数据放入列表中
        data = [(weather_dict[i].get('白天天气'), '白天天气'),
                (weather_dict[i].get('风力风向')[0], '风力风向'),
                (weather_dict[i].get('风力风向')[1], '风向'),
                (weather_dict[i].get('最高气温'), '最高气温'),
                (weather_dict[i].get('夜间天气'), '夜间天气'),
                (weather_dict[i].get('最低气温'), '最低气温')]

        group = LabelFrame(root1, text=weather_dict[i].get('日期'), padx=0, pady=0)  # 框架

        # group.pack(padx=11, pady=0, side='left')    # 放置框

        group.place(x=20+(i!=0)*15+i*120, y=125)

        for text, value in data:  # 将数据放入框架中
            c = Label(group, text=value + ': ' + str(text))
            c.pack(anchor=W)

    Label(root1, text='冬日天气寒冷，注意防寒保暖！', fg='green', font=("微软雅黑", 15)).place(x=300, y=30, height=50)  # 温馨提示

    Label(root1, text="Author: Kenny_ting", fg="black", bg="yellow").place(x=20, y=330, width=125, height=20)
    Button(root1, text='确认并退出', width=10, command=root1.quit).place(x=750, y=330, width=80, height=40)  # 退出按钮

    draw_line_chart(weather_dict)

    root1.mainloop()
