from get_weather_day_data import get_weather_day_data
from show_data import show_data


def get_weather_day(enter_text):
    url_list = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml',
    ]
    weather_dict = {}
    for url in url_list:
        res, weather_day_dict = get_weather_day_data(url, 0, enter_text)  # 得到当前城市今天的天气信息
        weather_dict[0] = weather_day_dict  # 保存数据
        if res is True:  # 当前的url不用变了，就是当前区域内
            for index in range(1, 7):
                res, weather_day_dict = get_weather_day_data(url, index, enter_text)
                weather_dict[index] = weather_day_dict
            break

    show_data(weather_dict, enter_text)  # GUI输出
