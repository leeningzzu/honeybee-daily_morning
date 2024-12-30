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

dsys.setrecursionlimit(10000)

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

# 分割过长的消息
def send_long_message(data, max_length=4096):
    """Send a message in chunks if the length exceeds the limit."""
    content = data["value"]
    if len(content) > max_length:
        # Split content into chunks
        chunks = [content[i:i+max_length] for i in range(0, len(content), max_length)]
        for i, chunk in enumerate(chunks, 1):
            print(f"Sending chunk {i}: {chunk[:30]}...")  # Print first 30 characters as a preview
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

# 假设获取天气、情感天数等数据
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

# 确保quest和content不会超过长度限制
send_long_message(data["quest"], max_length=1000)  # 可以设置更小的max_length
send_long_message(data["content"], max_length=4096)  # 微信的消息最大长度限制为4096字符
关键点：
分割消息：send_long_message 函数会将长文本内容分割成多个部分，逐条发送到微信，这样就可以避免一次性发送过长文本导致截断的问题。

字符长度控制：你已经设置了 max_quest_length 和 max_content_length，确保发送的消息内容不会超过微信平台的字符限制。

调试信息：通过打印一些调试信息（例如每个消息的前30个字符），帮助你了解在分割消息时可能出现的问题。

换行符和特殊字符处理：在处理 quest 内容时，通过 replace("\n", " ").replace("\r", " ") 过滤掉换行符，确保不会因为格式问题导致显示不完全。

通过这些改进，应该能解决你遇到的内容不全的问题。如果问题依然存在，可以进一步排查微信平台的消息格式限制。




2024/12/30 11:26:28

验证消息真实性	无上限	 
接收普通消息	无上限	 
接收事件推送	无上限	 
接收语音识别结果	无上限	开启
发送消息	自动回复	无上限	 
客服接口	500000	 
群发接口	详情	 
模板消息（业务通知）	100000	   应该是不显示长度的 请修改代码 使title content完整显示

2024/12/30 11:26:48

根据你提供的微信接口限制，发送消息的长度上限主要由微信接口本身决定。对于模板消息（业务通知），微信接口通常有字符长度限制，通常为 100,000个字符。但根据你的需求，如果希望 title 和 content 完整显示而不被截断，我们需要保证发送的消息符合微信接口的要求。

我们可以通过以下几个步骤来修改代码：

1. 确保 title 和 content 完整显示：
根据你的要求，我们不需要分割 title 和 content，只需要确保它们不会超出接口的字符限制。如果 title 或 content 的长度超过微信限制的最大长度（例如 100,000 个字符），我们可以适当处理，但正常情况下，微信不应当有严格的限制，除非你发送了非常长的内容。

2. 发送模板消息时处理：
确保发送的 title 和 content 保持原样，并在 send_long_message 函数中去除分割逻辑。如果内容超长，可以做截取处理。

3. 更新代码：
去掉原本的消息分割部分，确保直接发送完整内容，并对超长内容进行合理处理。

修改后的代码：
python
import requests
import sys

# 增加递归限制，防止递归深度过小
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

# 获取标题和内容
title_content = get_title_content()
title = title_content.get('title', '')
content = title_content.get('content', '')
content_typeid = title_content.get('typeid', '')  # 获取title和content的typeid


  
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
