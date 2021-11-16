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

def querySql(sql):
    config_dit = {
        'user': 'gmsweb',  # 数据库帐号
        'password': 'GDLNG1234',  # 数据库访问密码
        'host': '149.194.112.140',  # 数据库服务器IP
        'database': 'gmspdb04'  # 数据库名
    }

    def conn():
        connect = pymssql.connect(**config_dit)
        if conn:
            return connect
        else:
            print("Connected Failed.")

    connection = conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    row_value = row[0]
    return row_value
    cursor.close()
    connection.close()

def createPlot(dtq_total, dtq_yesterday_total, toq_total, toq_yesterday_total, accutoq_today, accutoq_yesterday, toq_yesterday_accu):
    int_hour = int(hour)
    x_hour = range(0, int_hour)
    x = np.array(x_hour)
    minus = accutoq_today-accutoq_yesterday
    y1 = np.array(dtq_total)
    y2 = np.array(dtq_yesterday_total)
    y3 = np.array(toq_total)
    y4 = np.array(toq_yesterday_total)
# pyplot的初始化参数
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = [15, 7]
    x_major_locator = MultipleLocator(1)
    y_major_locator = MultipleLocator(200)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(0, 1400)

    # for a, b in zip(x, y1):
    #     plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    plt.title("提气量曲线图")
    plt.xlabel("x - 小时")
    plt.ylabel("y - 气量（吨）")
    plt.grid(axis="y")

    plt.bar(x, y1, color=['#c5e0b4'], label='%s提气量' % today)
    plt.plot(x, y2, color='deepskyblue', marker='o', label='%s提气量' % yesterday)
    plt.bar(x, y3, color=['#f4b182'], label='%s出罐量' % today)
    plt.plot(x, y4, color='grey', marker='o', label='%s出罐量' % yesterday)
    plt.legend()
    if minus > 0:
        plt.annotate(xy=[2, 1200], color='red', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', ec='k', lw=1, alpha=0.4), s="截止至%d时,今日累计出罐较昨日增加%d吨" %(int_hour, minus))
    else:
        plt.annotate(xy=[2, 1200], color='red', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', ec='k', lw=1, alpha=0.4), s="截止至%d时,今日累计出罐较昨日减少%d吨" % (int_hour, -minus))

    plt.annotate(xy=[2, 1000], color='black', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', ec='k', lw=1, alpha=0.4), s="昨日出罐总量为%s吨" %(toq_yesterday_accu))
    file_name = 'D:/wehook_notification/wehook_pic/'+time.strftime("%Y-%m-%d%H%M%S", time.localtime())+'.jpg'
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
    # today_string = '2021-11-08'
    # today = datetime.datetime.strptime(today_string, '%Y-%m-%d').date()
    oneday = datetime.timedelta(days=1)
    yesterday = today-oneday
    hour = int(time.strftime("%H", time.localtime()))
    with open('D:/wehook_notification/urls.txt', 'r') as f:
        config = f.readlines()
        wehook_url = config[1]
    dtq_total = []
    dtq_yesterday_total = []
    toq_total = []
    toq_yesterday_total = []
    accutoq_today = 0
    accutoq_yesterday = 0

# 今日每小时提气量
    for i in range(hour):
        sql = """select SUM(isnull(Energy,0))/54.55 from gmspdb04.dbo.S2_HourlyStationBalance where + StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name <> 'HKCGB1' and Name <> 'TRN1' and Name <> 'SZLNG') 
            AND TIME='%s %s:00:00' """ % (today, i)
        dtq_today_mass = querySql(sql)
        dtq_total.append(dtq_today_mass)

# 昨日每小时提气量
    for i in range(hour):
        sql = """select SUM(isnull(Energy,0))/54.55 from gmspdb04.dbo.S2_HourlyStationBalance where + StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name <> 'HKCGB1' and Name <> 'TRN1' and Name <> 'SZLNG') 
            AND TIME='%s %s:00:00' """ % (yesterday, i)
        dtq_yesterday_mass = querySql(sql)
        dtq_yesterday_total.append(dtq_yesterday_mass)

# 今日每小时出罐量
    for i in range(hour):
        sql = """SELECT a.s-b.t from (select SUM(isnull(Energy,0))/54.55 s from gmspdb04.dbo.S2_HourlyStationBalance where + StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name <> 'HKCGB1' and Name <> 'TRN1' and Name <> 'SZLNG') 
 AND TIME='%s %s:00:00') a, (select SUM(isnull(Mass,0) / 1000) t  from gmspdb04.dbo.S2_HourlyStationBalance where StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name = 'SZLNG') AND TIME='%s %s:00:00') b;""" % (today, i, today, i)
        toq_today_mass = querySql(sql)
        toq_total.append(toq_today_mass)
    for h in toq_total:
        accutoq_today += int(h)

# 昨日每小时出罐量
    for i in range(hour):
        sql = """SELECT a.s-b.t from (select SUM(isnull(Energy,0))/54.55 s from gmspdb04.dbo.S2_HourlyStationBalance where + StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name <> 'HKCGB1' and Name <> 'TRN1' and Name <> 'SZLNG') 
    AND TIME='%s %s:00:00') a, (select SUM(isnull(Mass,0) / 1000) t  from gmspdb04.dbo.S2_HourlyStationBalance where StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name = 'SZLNG') AND TIME='%s %s:00:00') b;""" % (yesterday, i, yesterday, i)
        toq_yesterday_mass = querySql(sql)
        toq_yesterday_total.append(toq_yesterday_mass)
    for p in toq_yesterday_total:
        accutoq_yesterday += int(p)

# 昨日总出罐量
    sql = """SELECT a.s-b.t from (select SUM(isnull(Energy,0))/54.55 s from gmspdb04.dbo.S2_HourlyStationBalance where + StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name <> 'HKCGB1' and Name <> 'TRN1' and Name <> 'SZLNG') 
        AND CONVERT(VARCHAR(20),TIME,25) LIKE '%%%s%%') a, (select SUM(isnull(Mass,0) / 1000) t  from gmspdb04.dbo.S2_HourlyStationBalance where StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name = 'SZLNG') AND CONVERT(VARCHAR(20),TIME,25) LIKE '%%%s%%') b;""" % (yesterday, yesterday)
    toq_yesterday_accu = round(querySql(sql))

    f_name = createPlot(dtq_total, dtq_yesterday_total, toq_total, toq_yesterday_total, accutoq_today, accutoq_yesterday, toq_yesterday_accu)
    cvt_result = cvtbase64(f_name)
    jpg_base64 = cvt_result[0]
    jpg_md5 = cvt_result[1]
    result = webookRequest(wehook_url, jpg_base64, jpg_md5)



