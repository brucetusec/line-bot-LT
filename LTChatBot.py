
from last_nest import LastNest
from app_data import CONST_GPS, CONST_GPS_L, CONST_LAST_NEST_INFO, CONST_LAST_NEST_IDS, CONST_NEST_ZONE, CONST_GROUPS, CONST_NEST_GROUP_REMIND
import re
import sys
from data_preprocess import insert_whitespace, preprocess_text
class BotReply:
    def __int__(self):
        self.reply = ""
        self.send_reply = False

class LTChatBot:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.numbers = {}
        self.last_nest = LastNest()
        #self.last_nest.setData(CONST_LAST_NEST_INFO, CONST_LAST_NEST_IDS)
        #self.last_nest.parseInfo()

        self.bot_state = {}
        self.bot_state["last_reply"] = ""
        self.zones = CONST_NEST_ZONE.keys()
        for key in self.zones:
            if key in CONST_NEST_ZONE:
                self.load_old_nest(key, CONST_NEST_ZONE[key])        
        print("❗❗❗小幫手舊巢蛋數資料:0511 ❗❗❗")
        self.GPS_L_ON = True
        return
    def load_old_nest(self, zone, info):
        self.numbers[zone] = {}
        # remember the numbers
        matches = [_[0] for _ in re.findall(r'((N|L|KP|LR|SN)[0-9]{1,3})\b', info.upper())]
        for nest_id in matches:
            self.numbers[zone][nest_id] = 0
        return
    def handle_message(self, text, env):
        text = (text + "").upper()
        original_text = text
        text = (preprocess_text(text)+"").strip()
        first_word = text.split()[0]
    
        print("debug, text:[" + text + "]")
        sys.stdout.flush()
        reply_set = False
        zone_fit = False
        send_reply = False
        reply = ""
        if "關閉蘭陽" in text and "GPS" in text and "小幫手" in text:
            self.GPS_L_ON = False
        if "打開蘭陽" in text and "GPS" in text and "小幫手" in text:
            self.GPS_L_ON = True
        is_finding_nest = ("在哪" in text) or ("GPS" in text)
        if text == "小幫手 GPS":
            is_finding_nest = False
        if is_finding_nest:
            reply_set = True
            send_reply = False
            reply = ""
            if first_word in env['gps']:
                print("self.GPS_L_ON: ", self.GPS_L_ON)
                print("first_word  : [" + first_word + "]")
                # print("first_word in CONST_GPS_L: ", first_word in CONST_GPS_L)
                if not self.GPS_L_ON and env['group_name']=='蘭陽':
                    pass
                else:
                    latitude = env['gps'][first_word].split(',')[0].strip().strip('(').strip(')')
                    longitude = env['gps'][first_word].split(',')[1].strip().strip('(').strip(')')
                    google_map_url = f"https://www.google.com/maps?q={latitude},{longitude}"
                    reply = f"{first_word} 在這裡 {google_map_url}"
                    send_reply = True
            
        for zone in self.zones:
            if reply_set:
                continue
            if not zone in self.numbers:
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
        if zone_fit or reply_set:
            pass
            
        else:
            for zone in self.zones:
                if first_word in self.numbers[zone]:                    
                    self.numbers[zone][first_word] = 1
                    print("numbers[" + zone + "][" + first_word + "] is set")
                    sys.stdout.flush()
                    reply = "OK"
                    notify_zone_clear = CONST_NEST_ZONE.keys()
                    # ["第二區上","第二區下","GPS","過期","上次有雛","上週蛋數變少疑似成功",
                    #     "一巢區","溪口沙洲","獨立沙洲","孤草區",]
                    is_flag_removed = ("拔" in text or "收" in text or "失敗" in text or "成功" in text)
                    if zone.upper() == "GPS":
                        reply = "❗❗❗" + first_word + " 要重新定位❗❗❗"
                        send_reply = True
                    if zone.upper() == "過期" and not is_flag_removed:
                        reply = "❗❗❗" + first_word + " 過期失敗需收旗❗❗❗"
                        send_reply = True
                    if zone.upper() == "上次有雛":
                        reply = "❗" + first_word + " 上次有雛❗"
                        send_reply = True
                    if zone.upper() == "上週蛋數變少疑似成功":
                        reply = "❗" + first_word + " 上週蛋數變少疑似成功"
                        send_reply = True
                    
                    if zone.upper() == "中段一巢區需收旗" and not is_flag_removed:
                        reply = "❗❗❗" + first_word + " 需收旗❗❗❗"
                        send_reply = True
                    
                    if zone.upper() == "溪口段需收旗" and not is_flag_removed:
                        reply = "❗❗❗" + first_word + " 需收旗❗❗❗"
                        send_reply = True

                    new_eggs = self.last_nest.get_line_eggs(first_word, text)
                    
                    if reply=="OK" and not new_eggs=="":
                        old_eggs = self.last_nest.get_old_egg(first_word)
                        if not old_eggs == "" and not new_eggs==old_eggs:
                            if self.last_nest.is_alert(old_eggs, new_eggs):

                                eggs_array = ["一顆", "兩顆","三顆","四顆","五顆","六顆","七顆"]
                                eggs_array2 = ["1顆", "2顆","3顆","4顆","5顆","6顆","7顆"]
                                if old_eggs in eggs_array:
                                    for find_eg in range(len(eggs_array)):
                                        if old_eggs == eggs_array[find_eg]:
                                            old_eggs = eggs_array2[find_eg]

                                reply = first_word + " 上次是" + old_eggs
                                send_reply = True

                    if (zone in notify_zone_clear
                        and not ("全部完成" in self.numbers[zone]
                        and self.numbers[zone]["全部完成"] == 1)):
                            not_found = [num for num, found in self.numbers[zone].items() if found == 0]
                            if len(not_found) == 0:
                                self.numbers[zone]["全部完成"] = 1
                                if reply == "OK":
                                    reply = zone + "全部完成，收工！"
                                else:
                                    reply = reply + "\n" + zone + "全部完成，收工！"
                                send_reply = True
            if env['group_name'] in CONST_NEST_GROUP_REMIND:
                nest_is_ok = 0
                for zone in self.zones:
                    if first_word in self.numbers[zone]:
                        if self.numbers[zone][first_word] == 1:
                            nest_is_ok = 1
                if nest_is_ok:
                    for remind_message in CONST_NEST_GROUP_REMIND[env['group_name']]:
                        need_remind_nest_ids = CONST_NEST_GROUP_REMIND[env['group_name']][remind_message]
                        if first_word in need_remind_nest_ids:
                            need_remind_nest_ids.remove(first_word)
                            if reply == "OK":
                                reply = first_word + " " + remind_message
                            else:
                                reply = reply + "\n" + first_word + " " + remind_message
                            send_reply = True

        if not send_reply and text[:4] == "小幫手 ":
            reply = ("你可以用的指令:\r\n" +
                "-- 南澳 --\r\n" +
                "1)小幫手 沙灘區\r\n" +
                "2)小幫手 溪床區\r\n" +
                "3)小幫手 GPS\r\n" +
                "-- 蘭陽溪口 --\r\n" +
                "1)小幫手 溪口沙洲\r\n" +
                "2)小幫手 獨立沙洲\r\n" +
                "3)小幫手 草原區\r\n" +
                "4)小幫手 中段一巢區\r\n" +
                "5)小幫手 中段二巢區\r\n")

            send_reply = not (self.bot_state["last_reply"] == reply)
            send_reply = False

        
        result = BotReply()
        result.send_reply = send_reply
        result.reply = reply
        
        if send_reply:
            self.bot_state["last_reply"] = reply
        return result
        
                
