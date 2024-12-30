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

sys.setrecursionlimit(10000)

def get_title_content():
    url = "https://whyta.cn/api/tx/tenwhy?key=96f163cda80b&num=1"
    r = requests.get(url)
    response_json = r.json()

    result_list = response_json.get("result", {}).get("list", [])
    
    if result_list:
        title = result_list[0].get("title")
        content = result_list[0].get("content")
        typeid = result_list[0].get("typeid")  # 获取typeid

        # 打印标题和类型ID
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

def send_long_message(data, max_length=4096):
    """Send a message in chunks if the length exceeds the limit."""
    content = data["value"]
    if len(content) > max_length:
        # Split content into chunks
        chunks = [content[i:i+max_length] for i in range(0, len(content), max_length)]
        for chunk in chunks:
            print(f"Sending chunk: {chunk[:30]}...")  # Print first 30 characters as a preview
            # Here you would send the chunk to the actual service (e.g., wxpy or other messaging service)
            # For example: wm.send(chunk)
    else:
        print(f"Sending full content: {content[:30]}...")  # Print first 30 characters as a preview
        # Here you would send the full message: wm.send(data)

# 获取 naowan 数据和标题内容数据
quest_result = get_naowan_quest_result()
quest = quest_result.get('quest', '')
quest_typeid = quest_result.get('typeid', '')  # 获取对应的typeid

# 去掉可能的换行符
quest = quest.replace("\n", " ").replace("\r", " ")

# 如果需要，可以限制quest的最大长度
max_quest_length = 1000  # 根据需求调整最大长度
if len(quest) > max_quest_length:
    quest = quest[:max_quest_length]  # 截取前1000字符

# 获取标题和内容
title_content = get_title_content()
title = title_content.get('title', '')
content = title_content.get('content', '')
content_typeid = title_content.get('typeid', '')  # 获取title和content的typeid

# 限制content的长度，避免显示过长
max_content_length = 4096  # 微信消息最大长度为4096个字符
if len(content) > max_content_length:
    content = content[:max_content_length]  # 截取前4096字符
  
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
    },
    "content": {
        "value": content
    },
}
  
res = wm.send_template(user_id, template_id, data)
print(res)
