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
  
def get_daily_love():
    # 每日一句情话
    url = "https://api.lovelive.tools/api/SweetNothings/Serialization/Json"
    r = requests.get(url)
    all_dict = json.loads(r.text)
    sentence = all_dict['returnObj'][0]
    daily_love = sentence
    return daily_love
  
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
         "value":get_naowan_quest_result()['quest']
    },
 "result": {"value":get_naowan_quest_result()['result'] 
    },
}

  
res = wm.send_template(user_id, template_id, data)
print(res)
