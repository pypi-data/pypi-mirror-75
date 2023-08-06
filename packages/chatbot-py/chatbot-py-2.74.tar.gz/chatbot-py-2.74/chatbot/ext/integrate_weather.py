from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from dateutil import parser as date_parser
from datetime import date
import forecastio
import re
import time


api_key = "3b1a0ead7333234fe0b428ab4058c4cf"


class AddressError(Exception):
    """
    An exception to be raised when the address incorrect
    """

    def __init__(self, address):
        self.message = '地址"{}"输入有误'.format(address)
        super().__init__(self.message)


def get_weather(address, day):
    """
    :param str address: 地址
    :param str day: 时间, 格式为YYYYMMDD
    :return:
    """
    # 核查日期
    day = int(time.mktime(date_parser.parse(day).date().timetuple()))
    today = int(time.mktime(date.today().timetuple()))
    if day < today or day >= (today + 8 * 86400):
        return '只能查询8天内的天气情况'

    gps = Nominatim()
    location = None
    detail_address = ''
    # 获取地址的经纬度
    for i in range(5):
        try:
            location = gps.geocode(address)
        except (GeocoderTimedOut, GeocoderUnavailable):
            continue

        break

    if not location:
        raise AddressError(address)

    # 拼接详细地址信息
    for i in reversed(location.address.split(',')):
        match = re.search(r'[\u4e00-\u9fff]+', i)
        if match:
            detail_address += match.group()

    # 通过经纬度获取天气信息
    forecast = forecastio.load_forecast(api_key, location.latitude, location.longitude)
    all_daily_weather = forecast.daily().data
    daily_weather = None
    for weather in all_daily_weather:
        if weather.d.get('time') == day:
            daily_weather = weather
            break

    if not daily_weather:
        return '无法查询到该日期的天气情况'

    return {
        '详细地址': detail_address,
        '最低温度': round(daily_weather.temperatureMin),
        '最高温度': round(daily_weather.temperatureMax),
        # '总结': daily_weather.summary,
        '降雨概率': '{}%'.format(int(daily_weather.precipProbability * 100)),
        '日期': time.strftime('%Y-%m-%d', time.localtime(daily_weather.d.get('time')))
    }


if __name__ == '__main__':
    print(get_weather('青城山', '20190725'))
    print(get_weather('玄武湖', '20190725'))
    print(get_weather('秦淮河', '20190725'))
    print(get_weather('南京市雨花台区', '20190725'))
    print(get_weather('福州', '20190725'))
