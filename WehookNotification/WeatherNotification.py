# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import sys
import json


def weatherFetch(url):
    response = requests.get(url)
    if response.status_code == 200 and "err" not in response:
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print("该网站无法正常访问，请检查")
        sys.exit()
    weather = ''
    for child in soup.find('div', attrs={'class': "xml"}).children:
        weather = weather + child.get_text().strip() + '\n'
    print(weather)
    return weather

def wehookRequest(wehook_url, weather):
    if wehook_url == '':
        print("wehook的url地址为空！")
    else:
        data = {
    "msgtype": "text",
    "text": {
        "content": "%s" % weather,
    }
}
    data_json = json.dumps(data)
    response = requests.post(wehook_url, data=data_json)
    if response.status_code == 200 and 'err' not in response:
        print("天气消息发送成功")
        print(response)
    else:
        print("天气消息发送失败，请检查接口状态")
        sys.exit()


if __name__ == "__main__":
    url = "https://weather.cma.cn/web/channel-3780.html"
    wehook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2f3e52d7-c676-43ee-9867-19dc7324784c"
    weather = weatherFetch(url)
    # wehookRequest(wehook_url, weather)