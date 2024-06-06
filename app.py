
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import re
from datetime import datetime
from app_data import CONST_GROUPS, CONST_GPS

from LTChatBot import LTChatBot
# from app_data import CONST_GPS, CONST_LAST_NEST_INFO, CONST_LAST_NEST_IDS, CONST_NEST_ZONE, CONST_GROUPS
print("app start", datetime.now())

# datetime object containing current date and time
#now = 
#print("now =", now)
## dd/mm/YY H:M:S
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)
CHANNEL_ACCESS_TOKEN="tYwlAaQYoTCz/GHvwSb4fuGC2vK7vbzlpbabJpzxzgmuEUCt5VrN73m4T6cDEjjWTjbx7Ncpe5PxiF6uiDSQ+IbnbHTsNLJNp4wTfC2nKnGS9AqvvLO3t1j3gYEt2/PWopnjcsSYitYmv4nk1UZIfwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET="28dd0637edacefb7347eddee58849386"

app = Flask(__name__)

# Initialize LineBotApi with your Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# Initialize WebhookHandler with your Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

bots = {}
def get_env(event):
    # 取得群組 ID
    group_id = event.source.group_id
    group_name = ""
    try:
        group_summary = line_bot_api.get_group_summary(group_id)
        group_name = group_summary.group_name  # 群組名稱
        # print("Group Name:", group_name)
    except Exception as e:
        # 處理錯誤
        print("Error:", e)
    match_group_name = ""
    for key in CONST_GROUPS:
        if key in group_name:
            match_group_name = key
    group_name = match_group_name
    print('群組:' + group_name)
    if not group_name in bots:
        print('create bot with group_name:' + group_name)
        bots[group_name] = LTChatBot(line_bot_api)
    env = None
    if group_name:
        env = get_env_by_group_name(group_name)

    env['group_id'] = group_id
    return env

def get_env_by_group_name(group_name):
    env = {
        'group_name': group_name,
        'bot': bots[group_name],
        'gps': {},
    }
    if group_name in CONST_GPS:
        env['gps'] = CONST_GPS[group_name]
    return env

for group_name in CONST_GROUPS:
    if not group_name in bots:
        print('create bot with group_name:' + group_name)
        bots[group_name] = LTChatBot(line_bot_api)

@app.route("/home", methods=['GET'])
def home():
    # TODO: use env
    env = get_env_by_group_name('蘭陽')
    bot = bots['蘭陽']
    env['group_id'] = 'Ccda26746dc264948bee8bc6c7b845354' # group_id:Ccda26746dc264948bee8bc6c7b845354 測試群蘭陽

    # Get the current date and time
    now = datetime.now()
    # Format the date and time
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

    items = {}
    zone_content = ""
    for zone in bot.zones:
       msg = bot.handle_message(f"小幫手 {zone}", env).reply
       items[f"小幫手 {zone}"] = msg
       zone_content += f"{msg}<br/> <hr>"
       
    head = ""
    body = f"""2023 宜蘭小燕鷗調查小幫手<br/> {formatted_now} <br><hr><br>
    {zone_content}
    """

    return f'<html><head>{head}</head><body>{body}</body></html>'

@app.route("/live", methods=['GET'])
def live():
    return 'OK, v0701_1610'

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    env = get_env(event)
    if not env:
        print("env not found")
        return
    allow_group_ids = [
        'C9c9cd134327f047948521cb501c640d6', # group_id:C9c9cd134327f047948521cb501c640d6 測試群南澳
        'Ccda26746dc264948bee8bc6c7b845354', # group_id:Ccda26746dc264948bee8bc6c7b845354 測試群蘭陽
        'C8647aabcb3e83432a72ee92097d05922', # group_id:C8647aabcb3e83432a72ee92097d05922 小幫手測試區(3)
        'C385da56e176f8a212525675263ef61b8', # group_id:C385da56e176f8a212525675263ef61b8 0518蘭陽
        'Ca5a660292a54a3fc188d585954a5fa33', # group_id:Ca5a660292a54a3fc188d585954a5fa33 0518南澳

        'C823a789f4c931e9d60a61c73feba0715', # group_id:C823a789f4c931e9d60a61c73feba0715 0525蘭陽
        'Ce3296cf68613cadc36c14ed7c36932ca', # group_id:Ce3296cf68613cadc36c14ed7c36932ca 0526南澳

        'C79f61e92804e644e152af271de5caa4a', # group_id:C79f61e92804e644e152af271de5caa4a 0601南澳
        'Ca1cc456ea234125acde72c0eeed10284', # group_id:Ca1cc456ea234125acde72c0eeed10284 0602蘭陽
    ]
    if not env['group_id'] in allow_group_ids:
        print(f"group_id:{env['group_id']} with gruop_name:{env['group_name']} is not in white list")
    else:
        bot = env['bot']
        result = bot.handle_message(event.message.text, env)
        if result.send_reply:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=result.reply))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
