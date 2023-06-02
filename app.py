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
CHANNEL_ACCESS_TOKEN="tYwlAaQYoTCz/GHvwSb4fuGC2vK7vbzlpbabJpzxzgmuEUCt5VrN73m4T6cDEjjWTjbx7Ncpe5PxiF6uiDSQ+IbnbHTsNLJNp4wTfC2nKnGS9AqvvLO3t1j3gYEt2/PWopnjcsSYitYmv4nk1UZIfwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET="28dd0637edacefb7347eddee58849386"

app = Flask(__name__)

# Initialize LineBotApi with your Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# Initialize WebhookHandler with your Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

numbers = {}

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
    text = event.message.text
    first_word = (text+"").strip().split()[0]
    zones = ["第一區", "第三區", "第四區"]    
    zone_fit = False
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
            reply = "OK"
            print("[debug]", text, "OK", numbers)

        if not zone_fit and "小幫手" in text and (
                zone + "?" in text or 
                zone + "？" in text or
                zone == text[-len(zone):]
            ):
            zone_fit = True

            print("[debug] text:text:text:text:", text)
            # respond with numbers that haven't been found yet
            not_found = [num for num, found in numbers[zone].items() if found == 0]
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


        reply = ("你可以用的指令:\r\n" +
            "1)小幫手 第一區舊巢 N1 N2 N3...\r\n" +
            "2)小幫手 第一區?\r\n")

    if "小幫手" in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6601)
