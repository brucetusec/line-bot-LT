
from last_nest import LastNest
from app_data import CONST_LAST_NEST_INFO, CONST_LAST_NEST_IDS, CONST_NEST_ZONE
import re

from data_preprocess import insert_whitespace, preprocess_text
class BotReply:
    def __int__(self):
        self.reply = ""
        self.send_reply = False

class LTChatBot:
    def __init__(self):
        self.numbers = {}
        self.last_nest = LastNest()
        self.last_nest.setData(CONST_LAST_NEST_INFO, CONST_LAST_NEST_IDS)
        self.last_nest.parseInfo()

        self.bot_state = {}
        self.bot_state["last_reply"] = ""
        self.zones = ["第二區上", "第二區下", "GPS", "一巢區", "溪口沙洲", "獨立沙洲", "孤草區"]
        for key in self.zones:
            if key in CONST_NEST_ZONE:
                self.load_old_nest(key, CONST_NEST_ZONE[key])        
        return
    def load_old_nest(self, zone, info):
        self.numbers[zone] = {}
        # remember the numbers
        matches = [_[0] for _ in re.findall(r'((N|L|KP|LR|SN)[0-9]{1,3})\b', info.upper())]
        for nest_id in matches:
            self.numbers[zone][nest_id] = 0
        return
    def handle_message(self, text):

        text = (text + "").upper()
        original_text = text
        text = (preprocess_text(text)+"").strip()
        first_word = text.split()[0]
    
        print("debug, first_word:[" + first_word + "]")
        
        zone_fit = False
        send_reply = False
        reply = ""
        
        for zone in self.zones:
            if not zone in self.numbers:
                print('init zone:', zone)
                self.numbers[zone] = {}

            if not zone_fit and "小幫手" in text and zone + "舊巢" in text:
                zone_fit = True

                self.load_old_nest(zone, text)
                send_reply = True
                reply = "OK"

            if not zone_fit and "小幫手" in text and (text == f"小幫手 {zone}"):
                zone_fit = True
                # respond with numbers that haven't been found yet
                not_found = [num for num, found in self.numbers[zone].items() if found == 0]
                send_reply = True
                if len(not_found) == 0:
                    reply = zone + "全部完成，收工！"
                else:
                    not_found_N = len(not_found)
                    if not_found_N > 20:
                        not_found = not_found[:20]
                        reply = zone + f"還沒做的巢{not_found_N}個：" + " ".join(not_found) + "..."
                    else:
                        reply = zone + "還沒做的巢：" + " ".join(not_found)
                break
        if zone_fit:
            pass
            
        else:
            for zone in self.zones:
                if first_word in self.numbers[zone]:
                    self.numbers[zone][first_word] = 1
                    print("numbers[" + zone + "][" + first_word + "] is set")
                    reply = "OK"
                    if zone.upper() == "GPS":
                        reply = "❗❗❗" + first_word + " 要重新定位❗❗❗"
                        send_reply = True

                    new_eggs = self.last_nest.get_line_eggs(first_word, text)
                    
                    if reply=="OK" and not new_eggs=="":
                        old_eggs = self.last_nest.get_old_egg(first_word)
                        if not old_eggs == "" and not new_eggs==old_eggs:
                            if self.last_nest.is_alert(old_eggs, new_eggs):
                                reply = first_word + " 上次是" + old_eggs
                                send_reply = True

        if not send_reply and text[:4] == "小幫手 ":
            reply = ("你可以用的指令:\r\n" +
                "-- 南澳 --\r\n" +
                "1)小幫手 第二區上\r\n" +
                "2)小幫手 第二區下\r\n" +
                "3)小幫手 GPS\r\n" +
                "-- 蘭陽溪口 --\r\n" +
                "1)小幫手 一巢區\r\n" +
                "2)小幫手 溪口沙洲\r\n" +
                "3)小幫手 獨立沙洲\r\n" +
                "4)小幫手 孤草區\r\n")
            send_reply = not (self.bot_state["last_reply"] == reply)
            send_reply = False

        
        result = BotReply()
        result.send_reply = send_reply
        result.reply = reply
        
        if send_reply:
            self.bot_state["last_reply"] = reply
        return result
        
                
