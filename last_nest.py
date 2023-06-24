import re

def insert_whitespace(text):
    pattern = r'([A-Za-z0-9]+)([^A-Za-z0-9]+)'
    result = re.sub(pattern, r'\1 \2', text)

    
    pattern = r'([^A-Za-z0-9]+)([A-Za-z0-9]+)'
    result = re.sub(pattern, r'\1 \2', result)

    return result

CONST_LAST_NEST_INFO = """
05:57 玟淇 溪床區開始
05:57 凃仲蔚 Bruce SN36 失敗 收旗
06:02 玟淇 N159 兩顆
06:02 凃仲蔚 Bruce N79 兩顆
06:03 林如錦 KP26 三顆
06:03 凃仲蔚 Bruce N47 三顆
06:04 玟淇 N49 一顆
06:04 凃仲蔚 Bruce N50 兩顆
06:04 玟淇  N53 兩顆
06:04 凃仲蔚 Bruce N65 兩顆
06:05 玟淇 N51 兩顆
06:05 玟淇 N55 兩顆
06:06 玟淇 N48 兩顆
06:07 林如錦已收回訊息
06:08 玟淇 N52 兩顆
06:08 小燕鷗調查小幫手 N52 要重新定位
06:08 玟淇 24.4471826, 121.8074366
06:08 林如錦已收回訊息
06:09 玟淇 N62 一顆
06:09 凃仲蔚 Bruce 誰
06:09 玟淇 @林如錦 號碼？
06:10 玟淇 N69 一顆
06:10 凃仲蔚 Bruce N57 兩顆 疑似親鳥將巢蛋移動或是新巢
06:11 凃仲蔚 Bruce 圖片
06:11 林如錦 SN20失敗，收旗
06:12 玟淇 N54 兩顆
06:12 林如錦 N56 兩顆
06:12 小燕鷗調查小幫手 N56 要重新定位
06:12 凃仲蔚 Bruce 圖片
06:12 陳樹德 旁邊有舊巢痕跡嗎？
06:12 玟淇 N88 兩顆
06:12 凃仲蔚 Bruce 有
06:12 小燕鷗調查小幫手 N88 要重新定位
06:12 凃仲蔚 Bruce 老師到現場再研究
06:12 陳樹德 應該不會移巢
06:13 陳樹德 以前沒有這種狀況出現
06:13 玟淇 24.4471578, 121.8074923
06:14 陳樹德 圖片
06:14 陳樹德 N56上次有重複登記
06:14 玟淇 24.4471423, 121.8074993
06:14 林如錦 N66 一顆
06:15 凃仲蔚 Bruce N81 兩顆
06:16 凃仲蔚 Bruce 舊巢有需重新確認的我們有清單，會陸續補資料，最後再檢查一次
06:17 玟淇 N91 零蛋 判定失敗 拔旗
06:18 凃仲蔚 Bruce N80 兩顆
06:18 陳樹德 圖片
06:19 玟淇 N92 一顆
06:20 陳樹德 N57上週是新巢1顆，所以判定孵化成功，另一巢為新巢
06:20 凃仲蔚 Bruce N103 兩顆
06:20 陳樹德 圖片
06:20 玟淇 N93 兩顆
06:20 玟淇 N77 一顆
06:21 凃仲蔚 Bruce N103往南一顆新巢
06:21 玟淇 N157 兩顆
06:21 凃仲蔚 Bruce N102 兩顆
06:21 小燕鷗調查小幫手 N102 要重新定位
06:21 玟淇 N158 兩顆
06:22 玟淇 N110 兩顆
06:23 凃仲蔚 Bruce 24.4468480, 121.8073528
06:23 玟淇 N104 兩顆
06:23 林如錦 N63巢無蛋，記錄自5/28起，判斷成功，收旗
06:24 玟淇 N82 一顆
06:24 凃仲蔚 Bruce N63 成功
06:24 凃仲蔚 Bruce 數字跟後面中文空一格小幫手才能用
06:25 凃仲蔚 Bruce N105 兩顆
06:25 玟淇 N70 一顆
06:26 玟淇 N67 一顆
06:26 凃仲蔚 Bruce N83 兩顆
06:27 凃仲蔚 Bruce N84 兩顆
06:27 小燕鷗調查小幫手 N84 要重新定位
06:27 林如錦 N99 一顆
06:27 玟淇 N87 兩顆
06:27 凃仲蔚 Bruce N90 兩顆
06:28 玟淇 N156 兩顆
06:28 林如錦 N89 兩顆
06:28 小燕鷗調查小幫手 N89 要重新定位
06:28 凃仲蔚 Bruce 24.4469237, 121.8075238
06:28 玟淇 N100 兩顆
06:29 玟淇 N97 兩顆
06:30 玟淇 N153 兩顆
06:30 凃仲蔚 Bruce N58 一顆
06:30 玟淇 N151 兩顆
06:31 凃仲蔚 Bruce N112 2顆
06:31 玟淇 N86 兩顆
06:31 凃仲蔚 Bruce N107 兩顆
06:32 玟淇 N96 兩顆
06:32 凃仲蔚 Bruce N106 兩顆
06:32 玟淇 N98 兩顆
06:33 玟淇 N85 兩顆
06:33 凃仲蔚 Bruce N152 兩顆
06:33 小燕鷗調查小幫手 N85 要重新定位
06:33 林如錦 N95 兩顆
06:33 林如錦 N68 一顆
06:33 凃仲蔚 Bruce N109 兩顆
06:34 林如錦 N60 兩顆
06:34 玟淇 24.4468480, 121.8077789
06:34 凃仲蔚 Bruce N111 兩顆
06:34 林如錦 N59 兩顆
06:34 小燕鷗調查小幫手 N59 要重新定位
06:35 陳樹德 N45 一顆
06:36 凃仲蔚 Bruce 24.4469085, 121.8078537
06:40 玟淇 N76 一顆
06:40 凃仲蔚 Bruce N48 兩顆 24.4471209, 121.8073384
06:41 凃仲蔚 Bruce N55 兩顆 24.4471413, 121.8073260
06:41 林如錦 新N113 兩顆
06:42 林如錦 圖片
06:44 陳樹德 SN29 二顆
06:46 玟淇 N155 兩顆
正確位置：
24.4469088, 121.8071640
06:48 林如錦 新N114 一顆
06:48 林如錦 圖片
06:48 玟淇 KP28 三顆
06:52 玟淇 SN20 失敗，收旗
06:52 林如錦 新N115 兩顆
06:52 林如錦 圖片
06:56 林如錦 新N116 一顆
06:56 林如錦 圖片
06:59 玟淇 新 N117 兩顆
06:59 玟淇 圖片
07:04 玟淇 新 N118 兩顆
07:04 玟淇 圖片
07:05 林如錦 新N119 兩顆
07:05 林如錦 圖片
07:06 莊雅惠 小幫手我❤️你
07:08 陳樹德 N44 二顆
07:09 玟淇已收回訊息
07:09 玟淇 新 N154 兩顆
07:09 玟淇 圖片
07:09 林如錦 新N120 一顆
07:09 林如錦 圖片
07:10 陳樹德 N46 二顆
07:12 陳樹德 N41 二顆
07:13 楊錦秀 Kp27   三顆
07:14 陳樹德 N28 成功拔旗
07:15 玟淇 新 N160 兩顆
07:15 陳樹德 N42 二顆
07:15 玟淇 圖片
07:16 陳樹德 N43 二顆
07:17 陳樹德 N27 成功拔旗
07:19 陳樹德 N101 二顆
07:22 楊錦秀 N78成功拔旗
07:29 玟淇 新 N131 一顆
07:30 玟淇 圖片
07:32 玟淇 新 N132 三顆
07:32 玟淇 圖片
07:33 林如錦 新N136 兩顆
07:33 林如錦 圖片
07:34 陳樹德 新N141 二顆
07:34 陳樹德 圖片
07:36 玟淇 新 N133 兩顆
07:36 玟淇 圖片
07:40 莊雅惠 @楊錦秀 大姐，編號與字之間要有空隔，小幫手才能辨認，如「N78 成功拔旗」
07:42 莊雅惠 已新增新的記事本。
07:43 玟淇 正確位置
24.4468731, 121.8077035
07:45 林如錦 新N137 一顆
07:45 林如錦 圖片
07:46 玟淇 新 N134 兩顆
07:46 玟淇 圖片
07:46 玟淇 顏色不一樣
07:47 楊錦秀 Sn38   兩顆
07:47 小燕鷗調查小幫手 SN38 要重新定位
07:47 凃仲蔚 Bruce SN37 兩顆
07:48 莊雅惠 會不會剛生還沒變色？
07:49 莊雅惠 我以前養的鵪鶉剛生都很白不過一下子就變色了
07:50 凃仲蔚 Bruce 24.4470492, 121.8067741
07:52 莊雅惠 下次看一下就知道了~~
07:52 玟淇 新 N135 一顆
07:52 玟淇 圖片
07:53 凃仲蔚 Bruce N78 成功拔旗
07:55 陳樹德 SN37 二顆
07:57 凃仲蔚 Bruce SN28 一顆
07:57 凃仲蔚 Bruce SN27 一顆
08:00 玟淇 新 N138 兩顆
08:00 玟淇 圖片
08:06 已收回訊息
08:07 凃仲蔚 Bruce SN30 找不到旗子跟蛋
08:09 凃仲蔚 Bruce 圖片
08:10 陳樹德 新N142 一顆
08:10 凃仲蔚 Bruce 圖片
08:10 陳樹德 圖片
08:10 凃仲蔚 Bruce 花嘴鴨巢，被動物破壞
08:15 玟淇 N57 零蛋 判定失敗 拔旗
08:15 玟淇 新 N143 兩顆
08:15 玟淇 圖片
08:30 凃仲蔚 Bruce 圖片
08:31 楊錦秀 圖片
08:32 楊錦秀已收回訊息
08:33 凃仲蔚 Bruce 新N144 兩顆
08:36 楊錦秀 N139 兩顆
08:39 CH.LAI 新KP29 3顆
08:39 林如錦 新N140 兩顆
10:11 圖片
16:11 CH.LAI 早上近11點，堤防有人對溪床區拍攝，下午陸續有人來拍照，及開車至堤防盡頭。
16:30 陳樹德 我會再跟葉董提
如果是在堤防觀察小燕鷗的生態是ok，不要進入就好。
今天早上有人看到我們在調查，他怕是有人闖進去保護區，就打電話給葉董，葉董解釋是調查人員。
這樣反倒是好事，希望大家可以一起來監督。
16:35 CH.LAI 瞭解
"""

CONST_LAST_NEST_IDS = """N41 N42 N43 N44 N45 N46 N79 N101 N141 KP27 SN27 SN28 SN29 SN30 SN37 SN38 N47 N48 N49 N50 N51 N52 
N53 N54 N55 N56 N58 N59 N60 N62 N65 N66 N67 N68 N69 N70 N76 N77 N80 N81 N82 N83 N84 N85 N86 N87 N88 N90 N92 N93 N95 N96 
N97 N98 N99 N100 N102 N103 N104 N105 N106 N107 N109 N110 N111 N112 N113 N114 N115 N116 N117 N118 N119 N120 N131 N132 
N133 N134 N135 N136 N138 N140 N142 N143 N144 N151 N152 N153 N154 N155 N156 N157 N158 N159 N160 KP26 KP28 KP29 N89 N137 N139
"""
class LastNest:
    def __init__(self):
        self.data = ""
        self.last_ids = []
        self.old_eggs = {}

        for line in CONST_LAST_NEST_IDS.split("\n"):
            for word in line.split(' '):
                if len(word) > 0:
                    self.last_ids.append(word)
        #print(self.last_ids)

    def setData(self, input_data):
        self.data = input_data

    def parseInfo(self):
        self.old_eggs = {}
        valid_lines = []
        lines = self.data.split("\n")
        for line in lines:
            line = self.preprocess_line(line)
            line_arr = insert_whitespace(line).split(' ')
            line_arr = [_ for _ in line_arr if len(_) > 0]

            for nest_id in self.last_ids:
                if len(line_arr) < 5:
                    pass
                elif line_arr[3] == "小燕鷗調查小幫手":
                    pass
                elif nest_id in line_arr:
                    valid_lines.append(line)
                    the_index = -1
                    for m in range(len(line_arr)):
                        if line_arr[m] == nest_id:
                            the_index=m
                            break 
                    if the_index > -1:
                        egg_info = line_arr[the_index:the_index+2]                        
                        valid_lines.append(' '.join(egg_info))
                        self.old_eggs[egg_info[0]] = egg_info[1]
                        
        with open("output.txt", "w") as file:
            for line in valid_lines:
                file.write(line + "\n")

    def get_line_eggs(self, matched_nest, line):
        #print("debug: matched_nest/"+matched_nest, "line/"+line)
        line_arr = insert_whitespace(line).split(' ')
        the_index = -1
        for m in range(len(line_arr)):
            if line_arr[m] == matched_nest:
                the_index=m
                break
        eggs_info = ""
        if the_index > -1:
            eggs_info = ''.join(line_arr[the_index:])
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
        if not eggs_info in ["一顆", "兩顆","三顆","四顆","五顆","六顆","七顆",]:
            return ""
        return eggs_info

    def get_old_egg(self, nest):
        if nest in self.old_eggs:
            return self.old_eggs[nest]
        return ""

    def preprocess_line(self, line):
        line = line.replace("1顆", "一顆")
        line = line.replace("2顆", "兩顆")
        line = line.replace("二顆", "兩顆")
        line = line.replace("3顆", "三顆")
        line = line.replace("4顆", "四顆")
        line = line.replace("5顆", "五顆")
        line = line.replace("6顆", "六顆")
        line = line.replace("7顆", "七顆")
        return line