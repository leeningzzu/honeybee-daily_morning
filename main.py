from datetime import date, datetime
import math
import json
import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

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
  
def get_title_content():
    # 设置最大输出限制
    sys.setrecursionlimit(10000)  # 增加最大递归深度，避免输出被截断（一般情况下不需要）

    # 定义URL
    url = "https://whyta.cn/api/tx/tenwhy?key=96f163cda80b&num=1"
    
    # 发送GET请求
    r = requests.get(url)
    
    # 解析响应JSON数据
    response_json = r.json()
    
    # 获取返回数据中的第一个title和content
    result_list = response_json.get("result", {}).get("list", [])
    
    if result_list:  # 确保列表不为空
        title = result_list[0].get("title")
        content = result_list[0].get("content")
        
        # 打印标题和内容，确保内容不被截断
        print("Title:", title)
        print("Content:")
        print(content)  # 这里直接打印整个内容
        
        # 返回包含title和content的字典
        return {"title": title, "content": content}
    else:
        # 如果没有数据，返回None
        return {"title": None, "content": None}

# 调用函数并获取数据
get_title_content()
3. 保存到文件（如果内容非常长）：
如果内容特别长，或者你希望将长文本保存在文件中，以便更方便地查看，可以将 content 保存到文本文件中：

python
import requests
import json

def get_title_content():
    # 定义URL
    url = "https://whyta.cn/api/tx/tenwhy?key=96f163cda80b&num=1"
    # 发送GET请求
    r = requests.get(url)
    # 解析响应JSON数据
    response_json = r.json()
    # 获取返回数据中的第一个title和content
    result_list = response_json.get("result", {}).get("list", [])
    
    if result_list:  # 确保列表不为空
        title = result_list[0].get("title")
        content = result_list[0].get("content")
        
        # 打印标题
        print("Title:", title)
        
        # 将内容保存到文件
        with open("content.txt", "w", encoding="utf-8") as f:
            f.write(content)  # 将content写入文件
        
        print("Content has been saved to content.txt")
        
        # 返回包含title和content的字典
        return {"title": title, "content": content}
    else:
        # 如果没有数据，返回None
        return {"title": None, "content": None}

  
def get_naowan_quest_result():
    url = "https://whyta.cn/api/tx/naowan?key=96f163cda80b&num=1"
    r = requests.get(url)
    response_json = json.loads(r.text)
    
    # 获取返回数据中的第一个quest和result
    result_list = response_json["result"]["list"]
    if result_list:  # 确保列表不为空
        quest = result_list[0]["quest"]
        result = result_list[0]["result"]
        return {"quest": quest, "result": result}
    else:
        return {"quest": None, "result": None}  # 如果没有数据，返回None

quest_result = get_naowan_quest_result()
quest = quest_result.get('quest', '')
# 去掉可能的换行符
quest = quest.replace("\n", " ").replace("\r", " ")

# 如果需要，可以限制quest的最大长度
max_quest_length = 1000  # 根据需求调整最大长度
if len(quest) > max_quest_length:
    quest = quest[:max_quest_length]  # 截取前1000字符
  
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
    "today_note": {
         "value": get_daily_love()
    },
   "quest": {
        "value": quest
    },
 "result": {"value":get_naowan_quest_result()['result'] 
    },
   "title": {
        "value": get_title_content()['title'] 
    },
 "content": {"value":get_title_content()['content'] 
    },
}

  
res = wm.send_template(user_id, template_id, data)
print(res)
