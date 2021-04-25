from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import random


def get_news_title(url):
    """
    获取网页html
    """
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.130 Safari/537.36 "
    }

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option,后台运行
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    time.sleep(3)

    # ajax
    for i in range(7):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')  # 用html5lib解析器，去补全html标签

    title = []
    div_details = soup.find_all('div', {'class': 'detail'})
    for div_detail in div_details:
        h3 = div_detail.find('h3')  # 找到h3标签
        a = h3.find('a')  # 找到所有的a标签
        pattern = re.compile(r'<.*><.*><.*><.*><.*><.*>(.+)<.*></a>')
        title.append(pattern.findall(str(a)))
        title = list(filter(None, title))

    return title

