from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


def get_weather_day_data(url, index, city_name):  # 获取网站数据
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.130 Safari/537.36 "
    }

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option,后台运行
    driver = webdriver.Chrome(options=option)
    driver.get(url)

    result_list = driver.find_elements_by_xpath("//div/ul[@class='day_tabs']/li")  # 找到位置
    action = ActionChains(driver)
    action.move_to_element(result_list[index]).click().perform()  # 设置点击动作
    time.sleep(2)

    current_window = driver.current_window_handle  # 获取所有页面句柄
    all_Handles = driver.window_handles
    # 如果新的pay_window句柄不是当前句柄，用switch_to_window方法切换
    for window in all_Handles:
        if window != current_window:
            driver.switch_to.window(window)
            time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')  # 用html5lib解析器，去补全html标签

    div_hanml = soup.find('div', {'class': 'hanml'})
    conMidtabs = div_hanml.find_all('div', {'class': 'conMidtab'})
    tables = conMidtabs[index].find_all('table')  # 在conMidtab中找到所有table

    weather_day_dict = {}

    for table in tables:
        trs_all = table.find_all('tr')  # 所有的信息
        trs_info = trs_all[2:]  # 第一、二行是题头，没有天气信息

        for i, tr in enumerate(trs_info):  # 组合为一个索引序列
            ret = 0  # 取齐省份信息用
            tds = tr.find_all('td')  # 找到所有 td 开始的标签
            if i == 0:
                ret = 1
                province = tds[0]  # 省份

            city_td = tds[0 + ret]  # 城市名
            city = list(city_td.stripped_strings)[0]

            if city == city_name:  # 找到了

                print(result_list[index].text)  # 打印日期

                date = result_list[index].text  # 日期
                weather_day_td = tds[1 + ret]  # 白天天气现象
                wind_day_td = tds[2 + ret]  # 白天风向风力
                temp_day_td = tds[3 + ret]  # 白天气温
                weather_night_td = tds[4 + ret]
                wind_night_td = tds[5 + ret]
                temp_night_td = tds[6 + ret]

                city = list(city_td.stripped_strings)[0]
                weather_day = list(weather_day_td.stripped_strings)[0]
                wind_day = list(wind_day_td.stripped_strings)  # 风包括风向和风力
                temp_day = list(temp_day_td.stripped_strings)[0]
                weather_night = list(weather_night_td.stripped_strings)[0]
                wind_night = list(wind_night_td.stripped_strings)  # 风包括风向和风力
                temp_night = list(temp_night_td.stripped_strings)[0]
                print({"城市：": city})
                print({"白天 天气：": weather_day, " 风力风向：": wind_day, " 气温：": temp_day})
                print({"夜间 天气：": weather_night, " 风力风向：": wind_night, " 气温：": temp_night})
                weather_day_dict = {"白天天气": weather_day, "风力风向": wind_day, "最高气温": temp_day,
                                    "夜间天气": weather_night, "最低气温": temp_night, "日期": date}

                return True, weather_day_dict  # 找到了

    return False, weather_day_dict  # 没找到
