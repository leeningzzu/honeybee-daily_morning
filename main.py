from datetime import datetime
import os
import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
weather_key = os.getenv("WEATHER_API_KEY")

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

# 已抓取的 quest 集合，用于避免重复抓取
grabbed_quests = set()

def get_weather():
    url = f"https://api.seniverse.com/v3/weather/daily.json?key=S-3Yf85YRFz1MzNUS&location=beijing&language=zh-Hans&unit=c"
    res = requests.get(url).json()
    print(res)
    weather = res['results'][0]["daily"][0]
    return weather
  
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days

# 获取 naowan 数据
def get_naowan_quest_result():
    url = "https://whyta.cn/api/tx/naowan?key=96f163cda80b&num=1"
    r = requests.get(url)
    response_json = r.json()

    result_list = response_json.get("result", {}).get("list", [])
    
    last_typeid = None  # 用来记录上一个 typeid
    
    # 使用递归/循环来继续获取符合条件的 quest
    while result_list:
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
        
        # 如果没有符合条件的 quest，重新请求新数据
        print("未找到符合条件的 quest，重新请求数据...")
        r = requests.get(url)
        response_json = r.json()
        result_list = response_json.get("result", {}).get("list", [])
    
    # 如果没有符合条件的 quest，返回 None
    return None

# 获取标题和内容，确保符合字符限制
def get_title_content():
    url = "https://whyta.cn/api/tx/tenwhy?key=96f163cda80b&num=1"
    r = requests.get(url)
    response_json = r.json()

    result_list = response_json.get("result", {}).get("list", [])

    while result_list:
        for item in result_list:
            title = item.get("title")
            content = item.get("content")
            typeid = item.get("typeid")

            # 检查 title 是否超过 20 字符
            if len(title) > 20:
                print(f"title 长度超过 20 字，跳过: {title}")
                continue  # 跳过当前 title，继续查找下一个

            # 返回符合条件的 title 和 content
            return {"title": title, "content": content, "typeid": typeid}
        
        # 如果当前没有符合条件的 title，则重新请求数据
        print("未找到符合条件的 title，重新请求数据...")
        r = requests.get(url)
        response_json = r.json()
        result_list = response_json.get("result", {}).get("list", [])

    # 如果没有符合条件的 title，返回 None
    return None


# 获取 naowan quest 和 title 内容
quest_result = get_naowan_quest_result()
title_content = get_title_content()

# 如果 quest_result 或 title_content 为 None，表示未获取到新的 quest 或 title
if quest_result is None:
    print("未获取到新的 quest，跳过本次抓取。")
    exit()
else:
    quest = quest_result.get('quest', '')
    result = quest_result.get('result', '')
    quest_typeid = quest_result.get('typeid', '')  # 获取对应的 typeid

    # 清理 quest 中的换行符
    quest = quest.replace("\n", " ").replace("\r", " ")

if title_content is None:
    print("未获取到新的 title，跳过本次抓取。")
    exit()
else:
    title = title_content.get('title', '')
    content = title_content.get('content', '')
    content_typeid = title_content.get('typeid', '')

# 配置数据
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
        "value": result
    },
    "title": {
        "value": title
    },
    "content": {
        "value": content
    }
}

# 创建 WeChatClient 实例
client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

# 发送模板消息
res = wm.send_template(user_id, template_id, data)
print(res)
