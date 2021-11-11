# encoding: utf-8
import requests
import json
import pymssql
import pandas as pd
import time

def webookRequest(url, post_data):
    if url == '':
        print("url地址为空！")
    else:
        response = requests.post(url, data=post_data)
        response = response.json()
        response_str = json.dumps(response)
        print(response_str)
        if 'errcode' not in response_str:
            result = "发送成功"
            return result
        else:
            return 'Error'

def querySql():
    config_dit = {
        'user': 'gmsweb',  # 数据库帐号
        'password': 'GDLNG1234',  # 数据库访问密码
        'host': '149.194.112.140',  # 数据库服务器IP
        'database': 'gmspdb04'  # 数据库名
    }
    day = time.strftime("%Y-%m-%d")
    hour = time.strftime("%H", time.localtime())

    def conn():
        connect = pymssql.connect(**config_dit)
        if conn:
            print("Connected Successfully!")
            return connect
        else:
            print("Connected Failed.")

    connection = conn()
    cursor = connection.cursor()
    content = ''
    for i in range(int(hour)):
        sql = """select SUM(isnull(Energy,0))/54.55 from gmspdb04.dbo.S2_HourlyStationBalance where + StnId in (select Id from gmspdb04.dbo.S2_Stn where ObjTypeId=89 and Name <> 'HKCGB1' and Name <> 'TRN1' and Name <> 'SZLNG') 
            AND TIME='%s %s:00:00' """ % (day, i)
        cursor.execute(sql)
        row = cursor.fetchone()
        content.join(r"日期:%s , 气量:%s" % (day+ " "+ str(i) + ":00:00", row[0]))
    print(content)
    content = content.encode("utf-8")
    print("当前小时的提气量为：\n")
    outmsg = """{
    "msgtype": "text",
    "text": {
        "content": "%s"
    }
}""" %(content)
    print(outmsg)
    return outmsg # 返回查到的信息
    cursor.close()
    connection.close()


if __name__ == "__main__":
    webook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c14ed7e1-98b1-4eca-a3d1-0f392620789c"   # 这个是你要调用的机器人地址，在群里添加了机器人之后就会有这个地址了，每个机器人只有一个地址
    post_data = querySql()
    # result = webookRequest(webook_url, post_data)
    # print(result)
