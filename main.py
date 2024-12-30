from datetime import date, datetime
import math
import json
import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import sys 

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
weather_key = os.getenv("WEATHER_API_KEY")

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = f"https://api.seniverse.com/v3/weather/daily.json?key=S-3Yf85YRFz1MzNUS&location=beijing&language=zh-Hans&unit=c"
  res = requests.get(url).json()
  print(res)
  weather = (res['results'][0])["daily"][0]
  return weather
  
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days
  
#https://whyta.cn/api/tx/naowan?key=96f163cda80b&num=10

sys.setrecursionlimit(10000)

# 获取标题和内容
def get_title_content():
    url = "https://whyta.cn/api/tx/tenwhy?key=96f163cda80b&num=1"
    r = requests.get(url)
    response_json = r.json()

    result_list = response_json.get("result", {}).get("list", [])
    
    if result_list:
        title = result_list[0].get("title")
        content = result_list[0].get("content")
        typeid = result_list[0].get("typeid")  # 获取typeid

        print("Title:", title)
        print("Typeid:", typeid)

        # 将内容输出到文件
        with open("content_output.txt", "w", encoding="utf-8") as file:
            file.write(f"Title: {title}\n\n")
            file.write(f"Content:\n{content}")
        
        print("Content has been written to 'content_output.txt'.")

        return {"title": title, "content": content, "typeid": typeid}
    else:
        return {"title": None, "content": None, "typeid": None}

# 获取 naowan 数据
def get_naowan_quest_result():
    url = "https://whyta.cn/api/tx/naowan?key=96f163cda80b&num=1"
    r = requests.get(url)
    response_json = r.json()
    
    result_list = response_json.get("result", {}).get("list", [])
    if result_list:
        quest = result_list[0].get("quest")
        result = result_list[0].get("result")
        typeid = result_list[0].get("typeid")  # 获取对应的typeid
        return {"quest": quest, "result": result, "typeid": typeid}
    else:
        return {"quest": None, "result": None, "typeid": None}


# 获取 naowan 数据和标题内容数据
quest_result = get_naowan_quest_result()
quest = quest_result.get('quest', '')
quest_typeid = quest_result.get('typeid', '')  # 获取对应的typeid

# 去掉可能的换行符
quest = quest.replace("\n", " ").replace("\r", " ")

# 获取标题和内容
title_content = get_title_content()
title = title_content.get('title', '')
content = title_content.get('content', '')
content_typeid = title_content.get('typeid', '')  # 获取title和content的typeid

#    "content": {
#      "value": content
#  }
  
# 配置数据
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather = get_weather()
data = {
    "weather": {
        "value": weather['text_day'],
    },
    'tem_high': {
        "value": weather['high'],
    },
    "tem_low": {
        "value": weather['low'],
    },
    "love_days": {
        "value": get_count(),
    },
    "quest": {
        "value": quest
    },
    "result": {
        "value": quest_result['result']
    },
    "title": {
        "value": title
    }

}
  
res = wm.send_template(user_id, template_id, data)
print(res)
