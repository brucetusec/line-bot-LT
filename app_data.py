import re

CONST_LAST_NEST_INFO = """
"""

CONST_LAST_NEST_IDS = """
"""

CONST_GROUPS = [
    '蘭陽',
    '新城溪',
    '南澳',
    '和平',
]
CONST_NEST_ZONE = {
    "溪口沙洲":"""L21 L24 L6 L25 L26 KP1 KP9 KP7 KP6 KP8 KP5 KP10""",
    "獨立沙洲":"""""",
    "草原區":"""""",
    "中段第一巢區":"""""",
    "中段第二巢區":"""""",
    "沙灘區" : """SN1 SN4""",
    "溪床區": """""",

#南澳
# # "GPS":"SN46",
# # "過期": "N44 N155 N55",
# # "上次有雛":"",
# # "上週蛋數變少疑似成功":"",

#蘭陽
#"中段一巢區需收旗":"L286 L289 L291 L296 L300 L315 L333 L354 L358 L363 L369 L370 L371 L510",
#"溪口段需收旗":"L356 L381 L383 L390 L402 L403 L405 L406 L422 L423 L425 L427 L430 L432 L434 L437 L440 L442 L445 L447 L525 L530"

    }
def get_nests(data):
    result = []
    for word in data.split():
        result.append(word.upper())
    return result


REMOVED_NEST_L0701 = get_nests("""KP32 KP41 SN13 KP42 SN12 LR11 L224 L286 L310 L303 L280 L288 L301 L283 L313 L309 L308 L311 L320 L321 L314 L322
L290 L316 L323 L318 L317 L299 L312 L292 L293 L297 L279 L265 L295 L294 L298 L361 L324 L331 L332 L278 L325 L327
L366 L328 L362 L329 L380 L335 L365 L367 L368 L336 L337 L344 L334 L330 L347 L338 L339 L374 L340 L348 L342 L377
L393 L343 L341 L376 L391 L372 L349 L379 L352 L378 L351 L353 L358 L400 L375 L392 L355 L398 L357 L431 L433 L409
L434 L448 L444 L436 L401 L438 L423 L424 L426 L441 L429 L446 L428 L407 L382 L385 L388 L389 L387 L396 L397 L410
L394 L411 L373 L502 L503 L418 L504 L511 L513 L521 L514 L507 L523 L526 L527 L528 L484 L482 L487 L485""")
REMOVED_NEST_L0709 = get_nests("""KP5 KP11 LR11 KP24 LR12 LR22 KP24 KP31 KP41 KP32 KP33 KP35 KP41 LR24 KP43 SN13 KP42 KP45 SN12 KP53 KP52""")
REMOVED_NEST_N0709 = get_nests("""KP26 KP27 KP28 KP29 Sn47 N66 N70 N77 N81 N95 N100 N101 N102 N103 N104 N105 N106 N107 N110 N111 N112 N151 N152 N153 N156 N157 N158 N41 N42 N43 N45 N46 N47 N49 N50 N51 N53 N54 N60 N80 N82 N83 N86 N87 N89 N90 N97 N99 N109 N48 N52 N56 N59 N79 N84 N85 N88 N96 N98 N113 N114 N115 N116 N117 N118 N119 N120 N131 N133 N134 N136 N138 N139 N140 N141 N142 N143 N144 N154 N121 N122 N124 N145 N146 N148 N149 N150 N125 N162 N163 N164 N165 N167 N168 N169 N191 N192 N193 N194 N195 N196 N197 N198 N127 N128""")
# REMOVED_SET = set([] + REMOVED_NEST_L0701 + REMOVED_NEST_L0709 + REMOVED_NEST_N0709)
#  hardcode remove next
##  CONST_valid_nest_L = """KP34 KP44 SN14 SN15 SN21 SN22 L381 L505 L506 L416 L515 L491 L451 L465 L359 L414 L471 L415 L419 L461 L530 L493 L463 L481 L462 L467 L495 L468 L469 LR31 L476 L474 L537 L538 L536 L531 L464 L457 L454 L458 L459 L466 L475 L456 L477 L478 L480 L486 SN23 OS1"""
##  CHECK_valid_nest_L = {k:0 for k in get_nests(CONST_valid_nest_L)}
##  for key in CONST_NEST_ZONE.keys():
##      print(key, "old count:", len(CONST_NEST_ZONE[key].split()))
##      CONST_NEST_ZONE[key] = ' '.join([_ for _ in CONST_NEST_ZONE[key].split() if not _ in REMOVED_SET]    )
##      if key in ["一巢區","溪口沙洲","獨立沙洲","孤草區"]:
##          CONST_NEST_ZONE[key] = ' '.join([_ for _ in CONST_NEST_ZONE[key].split() if _ in CONST_valid_nest_L]    )
##      print(key, "new count:", len(CONST_NEST_ZONE[key].split()))
##      print(key, CONST_NEST_ZONE[key])

# for key in CONST_NEST_ZONE.keys():
#     print(key, " -- ", CONST_NEST_ZONE[key])
#     if key in ["一巢區","溪口沙洲","獨立沙洲","孤草區"]:
#         for nest in get_nests(CONST_NEST_ZONE[key]):
#             if not nest in CHECK_valid_nest_L:
#                 CHECK_valid_nest_L[nest] = 99
#             else: 
#                 CHECK_valid_nest_L[nest] = 1

# print("CHECK_valid_nest_L:")
# for k in CHECK_valid_nest_L.keys():
#     print(k, CHECK_valid_nest_L[k])
# exit()

CONST_LAST_NEST_IDS = []
for key in CONST_NEST_ZONE.keys():
    for word in CONST_NEST_ZONE[key].split():
        CONST_LAST_NEST_IDS.append(word.upper())

CONST_OLD_EGGS = {}

#import re

# 需要搜索的字串
#text = "時間 小幫手N1 L6 N01 KP11 KP101 KP67 KP 99 KP123 L456 L999 L1001 L101 L100"

# 進行正則表達式匹配
#matches = [_[0] for _ in re.findall(r'((N|L|KP|LR|SN)[0-9]{1,3})\b', text)]

# 輸出匹配結果
#print(matches)  

CONST_GPS = {"SN27" : "24.447709,121.805420",
"SN28" : "24.447769,121.805277", 
"N199" : "24.446948,121.807452",
"N201" : "24.446823,121.807661",
}
CONST_GPS_L = {
"L280": "24.715614,121.817504",   

}
CONST_GPS2={}
for k in CONST_GPS.keys():
    CONST_GPS2[k.upper()] = CONST_GPS[k]

for k in CONST_GPS_L.keys():
    CONST_GPS2[k.upper()] = CONST_GPS_L[k]
    
CONST_GPS=CONST_GPS2
# TODO : fix this feature
CONST_GPS = {}
