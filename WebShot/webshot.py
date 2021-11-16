from selenium import webdriver
import time
import os.path
import multiprocessing as mp
import base64
import json
import hashlib
import requests


def webshot(pic_name, url):
    print("当前进程%d已启动" % os.getpid())

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 不知为啥只能在无头模式执行才能截全屏
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    # 返回网页的高度的js代码
    js_height = "return document.body.clientHeight"

    try:
        driver.get(url)
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.2)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(pic_path)
        print("Process {} get one pic !!!".format(os.getpid()))
        driver.quit()
    except Exception as e:
        print(pic_name, e)
        exit()

def cvtbase64(pic_path):
    with open(pic_path, "rb") as f:
        fcont = f.read()
        pbase64 = base64.b64encode(fcont)
        pmd5 = hashlib.md5(fcont)
        return [pbase64, pmd5]

def wehookRequest(wehook_url, jpg_base64, jpg_md5):
    if wehook_url == '':
        print("wehookurl地址为空！")
    else:
        data = {"msgtype": "image", "image": {"base64": jpg_base64.decode('utf8'), "md5": jpg_md5.hexdigest()}}
        data_json = json.dumps(data)
        print("推送的json为%s" % data_json)
        response = requests.post(wehook_url, data=data_json)
        if 'errcode' not in response:
            print("发送成功")
        else:
            print("发送失败")
        return response.text


if __name__ == '__main__':
    # 首先创建一个保存截图的文件夹
    filename = "D:/wehook_notification/pics"

    if not os.path.isdir(filename):
        # 判断文件夹是否存在，如果不存在就创建一个
        os.makedirs(filename)

    # 读取保存url的文件，返回一个列表
    # 列表中每个元素都是一个元组，文件保存url的格式是：保存为图片的名称, 网页地址。
    # 例：baidu.png,https://www.baidu.com
    #     zhihu.png,https://www.zhihu.com
    with open('D:/wehook_notification/urls.txt', 'r') as f:
        config = f.readlines()
        weather_url = config[0]
        wehook_url = config[1]
        weather_url = weather_url.strip().split(",")
        if len(weather_url) == 2 and weather_url[0] and weather_url[1]:
            pic_name = weather_url[0]
            url = weather_url[1]
            pic_path = filename + '/' + pic_name
            webshot(pic_name, url)
        cvtresult = cvtbase64(pic_path)
        jpg_base64 = cvtresult[0]
        jpg_md5 = cvtresult[1]
        wehookRequest(wehook_url, jpg_base64, jpg_md5)



    # 创建进程池来多进程执行
    # pool = mp.Pool()
    # pool.map_async(func=webshot, iterable=urls)
    # pool.close()
    # pool.join()
