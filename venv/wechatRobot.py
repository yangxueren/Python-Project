import requests
import json

def main():
    webook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c14ed7e1-98b1-4eca-a3d1-0f392620789c"
    header = {"Content-Type": "application/json"}
    msg_text = {
        "msgtype": "text",
        "text": {
            "content": "[太阳]各位小伙伴，健康申报天天有约！[呲牙]\n [爱心]请点击以下链接\nhttps://www.wjx.cn/jq/55555555555357.aspx\n[嘿哈][嘿哈]",
            "mentioned_list":["@all"]
        }
    }
    msg_json = json.dumps(msg_text)
    response = requests.post(webook_url, data = msg_json)

if __name__ == "__main__":
    main()
