
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

print("app start", datetime.now())

# datetime object containing current date and time
#now = 
#print("now =", now)
## dd/mm/YY H:M:S
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)

from LTChatBot import LTChatBot
CHANNEL_ACCESS_TOKEN="tYwlAaQYoTCz/GHvwSb4fuGC2vK7vbzlpbabJpzxzgmuEUCt5VrN73m4T6cDEjjWTjbx7Ncpe5PxiF6uiDSQ+IbnbHTsNLJNp4wTfC2nKnGS9AqvvLO3t1j3gYEt2/PWopnjcsSYitYmv4nk1UZIfwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET="28dd0637edacefb7347eddee58849386"

app = Flask(__name__)

# Initialize LineBotApi with your Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# Initialize WebhookHandler with your Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

bot = LTChatBot()

@app.route("/home", methods=['GET'])
def home():
    
    # Get the current date and time
    now = datetime.now()
    # Format the date and time
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

    items = {}
    zone_content = ""
    for zone in bot.zones:
       msg = bot.handle_message(f"小幫手 {zone}").reply
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
    result = bot.handle_message(event.message.text)
    if result.send_reply:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result.reply))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
