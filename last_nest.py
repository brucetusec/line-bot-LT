import re
from data_preprocess import preprocess_text
from app_data import CONST_OLD_EGGS
class LastNest:
    def __init__(self):
        self.data = ""
        self.last_ids = []
        self.old_eggs = {}
        for key in CONST_OLD_EGGS.keys():
            eg = CONST_OLD_EGGS[key]
            eggs_array = ["一顆", "兩顆","三顆","四顆","五顆","六顆","七顆"]
            if eg in ["1","2","3","4","5","6","7"]:
                eg = eggs_array[int(eg) - 1]
            self.old_eggs[key] = eg
        

        #print(self.last_ids)

    def setData(self, input_data, last_nest_ids):
        self.last_ids = last_nest_ids + []
        # for line in last_nest_ids.split("\n"):
        #     for word in line.split(' '):
        #         if len(word) > 0:
        #             self.last_ids.append(word.upper())
        self.data = input_data

    def parseInfo(self):
        #self.old_eggs = {}
        valid_lines = []
        lines = self.data.split("\n")
        for line in lines:
            line = self.preprocess_line(line)
            line_arr = line.split(' ')
            line_arr = [_ for _ in line_arr if len(_) > 0]

            if len(line_arr) < 5:
                pass
            elif line_arr[3] == "小燕鷗調查小幫手":
                pass
            else:                
                matches = [_[0] for _ in re.findall(r'((N|L|KP|LR|SN)[0-9]{1,3})\b', line.upper())]
                for nest_id in matches: #self.last_ids:
                    if nest_id in line_arr:
                        index_of_nest_id_in_line = -1
                        for m in range(len(line_arr)):
                            if line_arr[m] == nest_id:
                                index_of_nest_id_in_line=m
                                break 
                        if index_of_nest_id_in_line > -1:
                            egg_info = line_arr[index_of_nest_id_in_line:index_of_nest_id_in_line+2]
                            #self.old_eggs[egg_info[0]] = (egg_info + [""])[1]
                        
        with open("output.txt", "w") as file:
            for line in valid_lines:
                file.write(line + "\n")

    def get_line_nest_id(self, line):
        line = self.preprocess_line(line)
        line_arr = line.split(' ')
        line_arr = [_ for _ in line_arr if len(_) > 0]

        if len(line_arr) < 4:
            pass
        elif line_arr[-1] == "圖片":
            pass
        elif line_arr[3] == "小燕鷗調查小幫手":
            pass
        else:

            line_arr_upper=[_.upper() for _ in line_arr]
            matches = [_[0] for _ in re.findall(r'((N|L|KP|LR|SN)[0-9]{1,3})\b', line.upper())]
            
            for nest_id in matches: #self.last_ids:
                if nest_id in line_arr_upper:
                    index_of_nest_id_in_line = -1
                    for m in range(len(line_arr)):
                        if line_arr_upper[m] == nest_id:
                            index_of_nest_id_in_line=m
                            break
                            
                    if index_of_nest_id_in_line > -1:                        
                        #egg_info = :index_of_nest_id_in_line+2]
                        return line_arr[index_of_nest_id_in_line].upper()#egg_info[0].upper()
        return ""

    def get_line_eggs(self, matched_nest, line, to_int=False):
        #print("debug: matched_nest/"+matched_nest, "line/"+line)
        line = line.replace("*", ",")
        line_arr = self.preprocess_line(line).split(' ')
        if line_arr[-1] == "新":
            line_arr = line_arr[:-1]
        the_index = -1
        for m in range(len(line_arr)):
            if line_arr[m].upper() == matched_nest.upper():
                the_index=m
                break

        possible_result = ["一顆", "兩顆","三顆","四顆","五顆","六顆","七顆",]
        eggs_info = ""
        if the_index > -1:
            eggs_info = line_arr[the_index] + ',' + (''.join(line_arr[the_index+1:]))
            eggs_info = eggs_info.upper()
            eggs_info = eggs_info.replace(",新", ",")
            eggs_info = eggs_info.replace("新", ",")
            eggs_info = eggs_info.replace(" ", "")
            eggs_info = eggs_info.replace(" ", "")
            eggs_info = eggs_info.replace(" ", "")
            
            eggs_info = "一顆" if "1顆" in eggs_info or "一顆" in eggs_info else eggs_info
            eggs_info = "兩顆" if "2顆" in eggs_info or "兩顆" in eggs_info else eggs_info
            eggs_info = "兩顆" if "二顆" in eggs_info else eggs_info
            eggs_info = "三顆" if "3顆" in eggs_info or "三顆" in eggs_info else eggs_info
            eggs_info = "四顆" if "4顆" in eggs_info or "四顆" in eggs_info else eggs_info
            eggs_info = "五顆" if "5顆" in eggs_info or "五顆" in eggs_info else eggs_info
            eggs_info = "六顆" if "6顆" in eggs_info or "六顆" in eggs_info else eggs_info
            eggs_info = "七顆" if "7顆" in eggs_info or "七顆" in eggs_info else eggs_info            
            if not eggs_info in possible_result:
                if f'{matched_nest},1' == eggs_info:
                    eggs_info = "一顆"
                elif f'{matched_nest},2' == eggs_info:
                    eggs_info = "兩顆"
                elif f'{matched_nest},3' == eggs_info:
                    eggs_info = "三顆"
                elif f'{matched_nest},4' == eggs_info:
                    eggs_info = "四顆"
                elif f'{matched_nest},5' == eggs_info:
                    eggs_info = "五顆"
                elif f'{matched_nest},6' == eggs_info:
                    eggs_info = "六顆"
                elif f'{matched_nest},7' == eggs_info:
                    eggs_info = "七顆"
                    
        if not eggs_info in possible_result:
            #print("debug get_line_eggs ", line_arr, " eggs_info:",  eggs_info)
            return ""

        if to_int:
            return 1 + possible_result.index(eggs_info)
        return eggs_info

    def get_old_egg(self, nest):
        if nest in self.old_eggs:
            return self.old_eggs[nest]
        return ""

    def preprocess_line(self, line):
        line = preprocess_text(line)
        line = line.replace("1顆", "一顆")
        line = line.replace("2顆", "兩顆")
        line = line.replace("二顆", "兩顆")
        line = line.replace("3顆", "三顆")
        line = line.replace("4顆", "四顆")
        line = line.replace("5顆", "五顆")
        line = line.replace("6顆", "六顆")
        line = line.replace("7顆", "七顆")
        return line

    def is_alert(self, old_eggs, new_eggs):
        if "雛" in old_eggs:
            return True

        eggs_array = ["一顆", "兩顆","三顆","四顆","五顆","六顆","七顆"]

        if old_eggs in eggs_array and new_eggs in eggs_array:
            old_eggs_index = eggs_array.index(old_eggs)
            new_eggs_index = eggs_array.index(new_eggs)
            if old_eggs_index > new_eggs_index:
                return True
        return False
    

