import requests
from bs4 import BeautifulSoup


# 该段代码用于实现从天气网站上爬取指定月每天的天气情况并写入指定的文件中
def main():
    header = {"cookies": "UM_distinctid=17cef662f2f4aa-05b1b1402dacd8-57b1a33-384000-17cef662f30d27; BAIDU_SSP_lcr=https://www.baidu.com/link?url=DjSqqkctBOBQugept4Wl29YOjvBDxHa-wHNkRyvFLdMT14iuVHkUwFgo5Olb2G0Q&wd=&eqid=8384b31e00090eaa0000000661877fe2; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1636172903,1636269827,1636269955,1636270040; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1636270067; CNZZDATA1259910480=159196047-1636157063-null%7C1636265071; Hm_lvt_b6bbdb7cf5398f3880daf0f6cd1e05db=1636158785,1636158795,1636158796,1636270081; Hm_lpvt_b6bbdb7cf5398f3880daf0f6cd1e05db=1636270081",
              "referer": "https://lishi.tianqi.com/",
              "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36"}

# 2020年1-12月的月份信息列表
    year = 2020
    month_list=[]
    for month in range(12):
        month_list.append("%d%02d" % (year, month+1))

# 查询每个月的天气页面信息
#     for i in month_list:
#     url = "https://m.tianqi.com/lishi/shenzhen/" + i + ".html"
    url = "https://m.tianqi.com/lishi/shenzhen/202001"
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    weather_list = soup.select('div[class="alioq"]')
    file = open('ShenZhen_Weather.txt', 'w')
    for weather in weather_list:
        for i in range(30):
            a = weather.select('a')[i]
            weather_date = a.select('div[class="wi190"]')[0].text
            tempratureMax = a.select('div[class="wi140 flex_cen"]')[0].text
            tempratureMin = a.select('div[class="wi140 flex_cen"]')[1].text
            weatherDetail = a.select('div[class="wi140 flex_cen"]')[2].text
            file.write(weather_date + '\t' + tempratureMax + '-' + tempratureMin + '\t' +weatherDetail + '\n')

    file.close()


if __name__ == "__main__":
    main()
