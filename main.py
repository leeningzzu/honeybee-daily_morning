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

# 用于保存已经抓取过的 quest 和 title
grabbed_quests = set()
grabbed_titles = set()

# 获取 naowan 数据
def get_naowan_quest_result():
    url = "https://whyta.cn/api/tx/naowan?key=96f163cda80b&num=1"
    r = requests.get(url)
    response_json = r.json()
    
    result_list = response_json.get("result", {}).get("list", [])
    
    last_typeid = None  # 用来记录上一个 typeid
    
    for item in result_list:
        quest = item.get("quest")
        result = item.get("result")
        typeid = item.get("typeid")  # 获取对应的 typeid

        # 如果 quest 长度超过 20 字，跳过该条数据
        if len(quest) > 20:  
            print(f"quest 长度超过 20 字，跳过: {quest}")
            last_typeid = typeid  # 记录当前 typeid
            continue  # 跳过当前 quest，继续查找下一个

        # 检查 quest 是否已抓取，避免重复
        if quest in grabbed_quests:
            print(f"重复的 quest，跳过: {quest}")
            continue

        # 将 quest 添加到已抓取的集合中
        grabbed_quests.add(quest)

        # 返回符合条件的 quest
        return {"quest": quest, "result": result, "typeid": typeid}
    
    # 如果没有符合条件的 quest，返回 None
    return None

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

        # 限制 title 长度为 20 字以内
        if len(title) > 20:  # 如果 title 长度超过20字，跳过
            print(f"title 长度超过 20 字，跳过: {title}")
            return None  # 跳过当前 title，返回 None

        # 检查 title 是否已抓取，避免重复
        if title in grabbed_titles:
            print(f"重复的 title，跳过: {title}")
            return None

        # 将 title 添加到已抓取的集合中
        grabbed_titles.add(title)

        print("Title:", title)
        print("Typeid:", typeid)

        # 将内容输出到文件
        with open("content_output.txt", "w", encoding="utf-8") as file:
            file.write(f"Title: {title}\n\n")
            file.write(f"Content:\n{content}")
        
        print("Content has been written to 'content_output.txt'.")

        return {"title": title, "content": content, "typeid": typeid}
    else:
        return None

# 配置数据并发送消息
def send_message(data):
    """发送消息到微信，确保title和content完整显示。"""
    
    # 获取 quest 和 content 的完整信息
    quest = data["quest"]["value"]
    content = data["content"]["value"]
    title = data["title"]["value"]
    
    # 确保 quest 和 content 不超长，如果确实超长则截取
    max_length = 100000  # 假设接口最大长度为 100000 字符（根据微信 API 的标准）

    if len(quest) > max_length:
        quest = quest[:max_length]
    if len(content) > max_length:
        content = content[:max_length]

    # 发送数据到微信接口，这里根据微信的客户端 API 进行发送
    # 假设 wm.send() 是发送消息的接口，这里你需要根据实际情况调用微信的发送接口
    # 下面为伪代码，实际情况需要替换为正确的调用方式
    print(f"Sending message with Title: {title[:30]}... and Content: {content[:30]}...")  # 调试信息
    # wm.send(data) # 替换为实际的消息发送代码

# 获取 naowan 数据和标题内容数据
quest_result = get_naowan_quest_result()

# 如果 quest_result 为 None，表示抓取到了重复的 quest 或未能获取到数据，跳过
if quest_result is None:
    print("未获取到新的 quest，跳过本次抓取。")
else:
    quest = quest_result.get('quest', '')
    quest_typeid = quest_result.get('typeid', '')  # 获取对应的 typeid

    # 去掉可能的换行符
    quest = quest.replace("\n", " ").replace("\r", " ")

    # 获取标题和内容
    title_content = get_title_content()

    # 如果没有获取到有效的 title，跳过
    if title_content is None:
        print("未获取到新的 title，跳过本次抓取。")
    else:
        title = title_content.get('title', '')
        content = title_content.get('content', '')
        content_typeid = title_content.get('typeid', '')  # 获取 title 和 content 的 typeid

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
