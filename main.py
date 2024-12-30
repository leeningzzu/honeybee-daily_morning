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
  
def get_words():
    words = requests.get("https://tenapi.cn/v2/yiyan?format=json").json()
    print(words)
    if words['code'] != 200:
        return get_words()
    return words['data']['hitokoto']
  
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

  
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
    "words": {
        "value": get_words(),
        "color": get_random_color()
    }
}

  
res = wm.send_template(user_id, template_id, data)
print(res)
