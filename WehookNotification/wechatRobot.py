# encoding: utf-8
import requests
import json
import pymssql
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import time
import datetime
import base64
import hashlib

def webookRequest(url, jpg_base64, jpg_md5):
    if url == '':
        print("url地址为空！")
    else:
        data = {"msgtype": "image", "image": {"base64": jpg_base64.decode('utf8'), "md5": jpg_md5.hexdigest()}}
        data_json = json.dumps(data)
        print("推送的json为%s" % data_json)
        response = requests.post(url, data=data_json)
        if 'errcode' not in response:
            print("发送成功")
        else:
            print("发送失败")
        return response.text
        # outmsg = """{
        #     "msgtype": "image",
        #     "image": {
        #         "base64": "%s",
        #         "md5": "%s"
        #     }
        # }""" %(jpg_base64, jpg_md5)
        # response = requests.post(url, data=outmsg)
        # response = response.json()
        # response_str = json.dumps(response)
        # print(response_str)
        # if 'errcode' not in response_str:
        #     result = "发送成功"
        #     return result
        # else:
        #     return 'Error'

def querySql():
    config_dit = {
        'user': 'gmsweb',  # 数据库帐号
        'password': 'GDLNG1234',  # 数据库访问密码
        'host': '149.194.112.140',  # 数据库服务器IP
        'database': 'gmspdb04'  # 数据库名
    }

    def conn():
        connect = pymssql.connect(**config_dit)
        if conn:
            print("Connected Successfully!")
            return connect
        else:
            print("Connected Failed.")

    connection = conn()
    cursor = connection.cursor()
    content1 = []
    content2 = []
    for i in range(int(hour)):
        sql = """select SUM(isnull(Energy,0))/54.55 from gmspdb04.dbo.S2_HourlyStationBalance where + StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name <> 'HKCGB1' and Name <> 'TRN1' and Name <> 'SZLNG') 
            AND TIME='%s %s:00:00' """ % (today, i)
        cursor.execute(sql)
        row = cursor.fetchone()
        row_value = row[0]
        content1.append(row_value)

    for i in range(int(hour)):
        sql = """select SUM(isnull(Energy,0))/54.55 from gmspdb04.dbo.S2_HourlyStationBalance where + StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name <> 'HKCGB1' and Name <> 'TRN1' and Name <> 'SZLNG') 
            AND TIME='%s %s:00:00' """ % (yesterday, i)
        cursor.execute(sql)
        row = cursor.fetchone()
        row_value = row[0]
        content1.append(row_value)
    # content = content.encode("utf-8")
    return [content1, content2]
    cursor.close()
    connection.close()


def createPlot(data_today, data_yesterday):
    int_hour = int(hour)
    x_hour = range(0, int_hour)
    x1 = np.array(x_hour)
    y1 = np.array(data_today)
    x2 = np.array(x_hour)
    y2 = np.array(data_yesterday)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    x_major_locator = MultipleLocator(1)
    y_major_locator = MultipleLocator(200)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(0, 1400)
    for a, b in zip(x1, y1):
        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(x2, y2):
        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    plt.title("今日提气量曲线图")
    plt.xlabel("x - 小时")
    plt.ylabel("y - 气量（吨）")
    plt.grid()
    plt.plot(x1, y1)
    plt.plot(x2, y2)
    file_name = 'D:/wehook_pic/'+time.strftime("%Y-%m-%d%H%M%S", time.localtime())+'.jpg'
    plt.savefig(file_name)
    return file_name


def cvtbase64(f1_name):
    with open(f1_name, "rb") as f:
        fcont=f.read()
        pbase64 = base64.b64encode(fcont)
        pmd5 = hashlib.md5(fcont)
        return [pbase64, pmd5]


if __name__ == "__main__":
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today-oneday
    hour = time.strftime("%H", time.localtime())
    # hour = 14
    wehook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c14ed7e1-98b1-4eca-a3d1-0f392620789c&debug=1"   # 这个是你要调用的机器人地址，在群里添加了机器人之后就会有这个地址了，每个机器人只有一个地址
    post_data = querySql()
    data_today = post_data[0]
    data_yesterday = post_data[1]
    f_name = createPlot(data_today, data_yesterday)
    cvt_result = cvtbase64(f_name)
    jpg_base64 = cvt_result[0]
    jpg_md5 = cvt_result[1]
    result = webookRequest(wehook_url, jpg_base64, jpg_md5)



