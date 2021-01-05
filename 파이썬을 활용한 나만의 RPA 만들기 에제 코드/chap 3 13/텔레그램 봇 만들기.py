import pandas as pd
import numpy as np

#
import requests
import json

#getMe
API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
url = "https://api.telegram.org/bot%s/getme" % API_TOKEN
r = requests.get(url)
result = json.loads(r.text)
print(result)

# getUpdates
url = "https://api.telegram.org/bot%s/getUpdates" % API_TOKEN
r = requests.get(url)
result = json.loads(r.text)
print(result)

# senMessage
chat_id = "XXXXXXXXXX"
chat_text = "안녕하세요? 저의 챗봇입니다"
url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (API_TOKEN, chat_id,  chat_text)
r = requests.get(url)
result = json.loads(r.text)
print(result)

# python-telemgram-bot 라이브러리로 메시지 보내기
#getMe
import telegram
import json

API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

bot = telegram.Bot(token = API_TOKEN)
print(bot.getMe())

# getUpdates
updates = bot.getUpdates()
print(updates[0])

# 사용자(보낸 사람) chat_id 얻기 
msg = updates[0].message
print(msg.chat.last_name, msg.chat.first_name)

chat_id = msg.chat.id 
print(chat_id)

# 간단한 메시지 송신

bot.sendMessage(chat_id=chat_id, text="안녕? 저는 로봇 입니다.")

# 마크다운

text="다양한 마크다운 텍스트를 전공할 수 있습니다.\n 일반 텍스트 *강조 텍스트* _이탤릭 텍스트_"
bot.sendMessage(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

# 마크다운 링크

text="BotFather의 링크입니다.. [BotFather](https://telegram.me/BotFather)"
bot.sendMessage(chat_id=chat_id, text=text)