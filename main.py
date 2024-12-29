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

def get_weather(key):
  url = f"https://api.seniverse.com/v3/weather/daily.json?key={key}&location=beijing&language=zh-Hans&unit=c"
  res = requests.get(url).json()
  print(res)
  weather = (res['results'][0])["daily"][0]
  return weather
  
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days
  
def add_spaces(text, interval=20):
    return ' '.join(text[i:i+interval] for i in range(0, len(text), interval))
  
def get_words():
  words = requests.get("https://api.52vmy.cn/api/wl/s/jzw")
  if words.status_code != 200:
    return get_words()
  return add_spaces(words.json()['data']['text'])
  
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather = get_weather(weather_key)
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
