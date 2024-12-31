import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import os
from datetime import datetime

# 获取当前日期
today = datetime.now()

# 环境变量
start_date = os.environ['START_DATE']
city = os.environ['CITY']
weather_key = os.getenv("WEATHER_API_KEY")

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id1 = os.environ["USER_ID1"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]

# 获取天气信息
def get_weather():
    url = f"https://api.seniverse.com/v3/weather/daily.json?key={weather_key}&location={city}&language=zh-Hans&unit=c"
    res = requests.get(url).json()
    weather = res['results'][0]["daily"][0]
    return weather

# 获取从开始日期到今天的天数
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days

# 获取 naowan 任务结果，确保同一 typeid 下 quest 和 result 符合字符限制
def get_naowan_quest_result():
    url = "https://whyta.cn/api/tx/naowan?key=96f163cda80b&num=1"
    r = requests.get(url)
    response_json = r.json()

    result_list = response_json.get("result", {}).get("list", [])

    while result_list:
        for item in result_list:
            quest = item.get("quest")
            result = item.get("result")
            typeid = item.get("typeid")

            # 检查 quest 和 result 是否都在 20 字符以内
            if len(quest) > 20 or len(result) > 20:
                print(f"quest 或 result 长度超过 20 字，跳过 typeid: {typeid}")
                continue  # 跳过该 typeid，继续查找下一个

            # 返回符合条件的 quest 和 result
            return {"quest": quest, "result": result, "typeid": typeid}
        
        # 如果当前没有符合条件的 quest，则重新请求数据
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

# 发送消息到微信，确保quest、title、content长度不超过20个字符
def send_message(data, user_id):
    """发送消息到微信，确保quest、title、content长度不超过20个字符。"""
    
    # Extract quest, content, and title
    quest = data.get("quest", {}).get("value", '')
    content = data.get("content", {}).get("value", '')
    title = data.get("title", {}).get("value", '')

    # Ensure quest, content, and title do not exceed 20 characters
    if len(quest) > 20:
        quest = quest[:20]
    if len(content) > 20:
        content = content[:20]
    if len(title) > 20:
        title = title[:20]

    # Prepare data for message
    message_data = {
        "weather": {
            "value": data["weather"]
        },
        'tem_high': {
            "value": data['tem_high']
        },
        "tem_low": {
            "value": data['tem_low']
        },
        "love_days": {
            "value": data['love_days']
        },
        "quest": {
            "value": quest
        },
        "result": {
            "value": data['result']
        },
        "title": {
            "value": title
        },
       "content": {
            "value": content
        }
    }

    # Create WeChat client and send message to user
    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)
    res = wm.send_template(user_id, template_id, message_data)
    print(f"Message sent to {user_id}: {res}")

# 发送消息给多个用户
def send_messages_to_users(data, user_ids):
    for user_id in user_ids:
        send_message(data, user_id)

# 主逻辑
def main():
    # 获取 quest 和 title 内容
    quest_result = get_naowan_quest_result()
    title_content = get_title_content()

    # 如果 quest_result 为 None，表示未获取到新的 quest
    if quest_result is None:
        print("未获取到新的 quest，跳过本次抓取。")
        return
    else:
        quest = quest_result.get('quest', '')
        quest_typeid = quest_result.get('typeid', '')  # 获取对应的 typeid

        # 清理 quest 中的换行符
        quest = quest.replace("\n", " ").replace("\r", " ")

    # 获取标题和内容
    if title_content is None:
        print("未获取到新的 title，跳过本次抓取。")
        return
    else:
        title = title_content.get('title', '')
        content = title_content.get('content', '')
        content_typeid = title_content.get('typeid', '')

    # 准备发送的消息数据
    weather = get_weather()
    data = {
        "weather": weather['text_day'],
        'tem_high': weather['high'],
        "tem_low": weather['low'],
        "love_days": get_count(),
        "quest": {
            "value": quest
        },
        "result": {
            "value": quest_result.get('result', '')
        },
        "title": {
            "value": title
        },
        "content": {
            "value": content
        }
    }

    # 获取用户 ID 列表并发送消息
    user_ids = [user_id1, user_id2]
    send_messages_to_users(data, user_ids)

# 执行主逻辑
if __name__ == "__main__":
    main()
