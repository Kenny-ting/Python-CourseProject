from NewsData import get_news_title
from word_analysis import word_count
from tkinter import *
from DataShow import show_data

# 需要爬取的链接：经济、娱乐、军事、科技、国际
# url_list = ['https://news.qq.com/',            # 要闻
#             'https://new.qq.com/ch/antip/',    # 抗肺炎
#             'https://new.qq.com/ch/finance/',  # 财经
#             'https://new.qq.com/ch/ent/',      # 娱乐
#             'https://new.qq.com/ch/milite/',   # 军事
#             'https://new.qq.com/ch/tech/',     # 科技
#             'https://new.qq.com/ch/world/'     # 国际
#             ]

global root


def win_quit():
    global root
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.destroy()


def get_url(news_type):

    url = "https://new.qq.com/"
    url_ending = ""

    if news_type == "要闻":
        url_ending = ""
    elif news_type == "抗肺炎":
        url_ending = "ch/antip/"
    elif news_type == "财经":
        url_ending = "ch/finance/"
    elif news_type == "娱乐":
        url_ending = "ch/ent/"
    elif news_type == "军事":
        url_ending = "ch/milite/"
    elif news_type == "科技":
        url_ending = "ch/tech/"
    elif news_type == "国际":
        url_ending = "ch/world/"

    url += url_ending
    return url


def main():
    # 输入窗口
    global root
    root = Tk()
    root.title('腾讯新闻')  # 窗口标题
    Label(root, text='  新闻板块:').grid(row=0, column=0)  # 设置标签并调整位置
    enter = Entry(root)  # 输入框
    enter.grid(row=0, column=1, padx=20, pady=20)  # 调整位置
    enter.delete(0, END)  # 清空输入框
    enter.insert(0, '抗肺炎')  # 设置默认文本
    enter_text = enter.get()  # 获取输入框的内容

    # 布置按键
    Button(root, text="查询", width=10, command=lambda: win_quit()) \
        .grid(row=3, column=1, sticky=E, padx=10, pady=5)

    root.mainloop()  # the main thread

    news_type = enter_text
    print("========================== {} ==========================".format(news_type))

    url = get_url(news_type)     # 根据输入得到网站的url
    title = get_news_title(url)  # 根据url得到新闻热点标题列表

    print(title)
    print("爬取完毕！")

    print("=================")
    print("开始词频统计")
    word_data = word_count(title)

    print("统计完毕!")

    show_data(word_data, news_type)


if __name__ == '__main__':
    main()
