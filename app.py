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
from last_nest import LastNest, CONST_LAST_NEST_INFO
import re

def insert_whitespace(text):
    pattern = r'([A-Za-z0-9]+)([^A-Za-z0-9]+)'
    result = re.sub(pattern, r'\1 \2', text)
    return result

CHANNEL_ACCESS_TOKEN="tYwlAaQYoTCz/GHvwSb4fuGC2vK7vbzlpbabJpzxzgmuEUCt5VrN73m4T6cDEjjWTjbx7Ncpe5PxiF6uiDSQ+IbnbHTsNLJNp4wTfC2nKnGS9AqvvLO3t1j3gYEt2/PWopnjcsSYitYmv4nk1UZIfwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET="28dd0637edacefb7347eddee58849386"

app = Flask(__name__)

# Initialize LineBotApi with your Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# Initialize WebhookHandler with your Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

numbers = {}
bot_state = {}
bot_state["last_reply"] = ""

last_nest = LastNest()
last_nest.setData(CONST_LAST_NEST_INFO)
last_nest.parseInfo()

@app.route("/live", methods=['GET'])
def live():
    return 'OK'

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
    text = (event.message.text + "").upper()
    print("debug, insert_whitespace:[" + insert_whitespace(text) + "]")
    first_word = (insert_whitespace(text)+"").strip().split()[0]
    print("debug, first_word:[" + first_word + "]")
    
    zones = ["第二區上", "第二區下", "GPS", "第四區"]    
    zone_fit = False
    send_replay = False
    for zone in zones:
        if not zone in numbers:
            print('init zone:', zone)
            numbers[zone] = {}

        if not zone_fit and "小幫手" in text and zone + "舊巢" in text:
            zone_fit = True

            numbers[zone] = {}
            # remember the numbers
            nums = text.split()[1:]
            for num in nums:
                if not num==zone + "舊巢":
                    numbers[zone][num] = 0
            send_replay = True
            reply = "OK"

        if not zone_fit and "小幫手" in text and (
                zone + "?" in text or 
                zone + "？" in text or
                zone == text[-len(zone):]
            ):
            zone_fit = True
            # respond with numbers that haven't been found yet
            not_found = [num for num, found in numbers[zone].items() if found == 0]
            send_replay = True
            if len(not_found) == 0:
                reply = zone + "全部完成，收工！"
            else:
                reply = zone + "還沒做的巢：" + " ".join(not_found)

            break
    if zone_fit:
        pass
        
    else:
        for zone in zones:
            if first_word in numbers[zone]:
                # mark the numbers as found
                numbers[zone][first_word] = 1
                print("numbers[" + zone + "][" + first_word + "] = 1")
                reply = "OK"
                if zone.upper() == "GPS":
                    reply = first_word + " 要重新定位"
                    send_replay = True

                new_eggs = last_nest.get_line_eggs(first_word, insert_whitespace(text))
                
                if replay=="OK" and not new_eggs=="":
                    old_egg = last_nest.get_old_egg(first_word)
                    if not old_egg == "" and not new_eggs==old_egg:
                        replay = first_word + " 上次是 " + last_eggs
                        send_replay = True

    if not send_replay and text[:4] == "小幫手 ":
        reply = ("你可以用的指令:\r\n" +
            "1)小幫手 第二區上\r\n" +
            "2)小幫手 第二區下\r\n" +
            "2)小幫手 重新定位\r\n")
        send_replay = not (bot_state["last_reply"] == reply)
        
    if send_replay:
        bot_state["last_reply"] = reply
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
