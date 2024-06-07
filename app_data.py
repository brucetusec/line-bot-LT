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
    "溪口沙洲":"""KP15,KP25,KP5,L102,L165,L169,L170,L19,L2,L207,L220,L235,L247,L249,L262,L270,L284,L287,L288,L291,L294,L295,L302,L304,L310,L318,L339,L342,L354,L366,L393,L401,L405,L71,L74,KP6,L13,L134,L15,L156,L164,L176,L201,L205,L212,L238,L242,L261,L263,L272,L277,L3,L303,L341,L355,L371,L50,L57,L7,L113,L125,L159,L184,L188,L196,L225,L245,L251,L265,L269,L4,L40,L44,L76,L85,KP22,KP23,L12,L132,L133,L135,L136,L147,L152,L154,L155,L160,L166,L168,L174,L178,L182,L185,L186,L187,L189,L190,L193,L195,L197,L199,L206,L208,L209,L210,L214,L216,L218,L219,L223,L224,L226,L227,L231,L233,L234,L239,L240,L241,L246,L250,L253,L254,L255,L257,L258,L259,L260,L267,L268,L271,L274,L275,L276,L278,L279,L280,L282,L283,L285,L286,L290,L292,L293,L296,L297,L301,L305,L306,L309,L311,L312,L314,L315,L319,L320,L321,L322,L330,L331,L332,L333,L334,L335,L336,L337,L351,L352,L353,L357,L358,L361,L362,L363,L364,L365,L367,L369,L370,L372,L373,L374,L375,L391,L392,L394,L402,L403,L404,L406,L407,L408,L192,L203,L27,L106,L14,L148,L157,L18,L202,L232,L264,L47,L5,L55,L56,L64,L73,L87,L88,L99,KP11,KP12,KP16,KP18,KP27,KP28,KP29,KP31,L139,L158,L163,L175,L179,L180,L194,L198,L215,L217,L228,L229,L237,L243,L248,L252,L256,L273,L30,L308,L313,L316,L317,L338,L376,L381,L395,L46,L66,L8,L93,L183,L72,L87,L88,L93,L99
""",
    "獨立沙洲":"""""",
    "草原區":"""""",
    "中段第一巢區":"""""",
    "中段第二巢區":"""""",
    "沙灘區" : """
        N10,N11,N19,N20,
        SN1,SN8,SN9,
        KP4,KP5,KP7,KP8
    """,
    "溪床區": """SN3,SN7,SN12,LR7""",
    "北岸沙洲": """KP2,KP3,KP6,N1,N100,N101,N102,N103,N104,N105,N106,N107,N108,N109,N110,N112,N113,N114,N115,N116,N117,N118,N119,N12,N120,N121,N122,N124,N125,N126,N127,N129,N13,N130,N132,N14,N15,N16,N17,N18,N194,N196,N198,N21,N23,N24,N25,N27,N28,N29,N3,N30,N33,N34,N35,N37,N39,N4,N41,N42,N44,N45,N46,N47,N48,N49,N5,N50,N51,N52,N53,N54,N55,N56,N57,N58,N59,N6,N60,N61,N63,N64,N65,N66,N67,N68,N69,N7,N70,N71,N72,N73,N74,N75,N76,N77,N78,N79,N8,N80,N81,N82,N83,N84,N85,N86,N87,N88,N89,N9,N90,N91,N92,N93,N94,N96,N97,N98,N99
""",
#南澳
# # "GPS":"SN46",
# # "過期": "N44 N155 N55",
# # "上次有雛":"",
# # "上週蛋數變少疑似成功":"",

#蘭陽
#"中段一巢區需收旗":"L286 L289 L291 L296 L300 L315 L333 L354 L358 L363 L369 L370 L371 L510",
#"溪口段需收旗":"L356 L381 L383 L390 L402 L403 L405 L406 L422 L423 L425 L427 L430 L432 L434 L437 L440 L442 L445 L447 L525 L530"

    }
CONST_NEST_GROUP_REMIND = {
    "蘭陽":{
        # "❗❗❗需補表單資料❗❗❗": ["L274"],
    },
    "南澳":{
        # "❗❗❗請重新定位 GPS 貼在群組❗❗❗": ["SN3"],
        # "❗❗❗需補表單資料❗❗❗": ["N70"],
        # "❗❗❗如果蛋還在請將旗與蛋補拍照再將旗插回❗❗❗": ["SN10"],
        # "❗❗❗請拍蛋照片上傳群組❗❗❗": ["N42"],
    }
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

CONST_GPS = {
    "SN1" : "24.447709,121.805420",
    "SN2" : "24.447769,121.805277",
    "SN3" : "24.446948,121.807452",
    "SN4" : "24.446823,121.807661",
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
CONST_GPS['蘭陽'] = {
'KP1':'24.7014341,121.8259274',
'KP2':'24.7101468,121.8364833',
'KP3':'24.7016872,121.8259606',
'KP4':'24.7095904,121.8364631',
'L21':'24.7093254,121.8369503',
'KP9':'24.7094953,121.8369050',
'KP7':'24.709167,121.836111',


'L24':'24.711379,121.836587',
'L6':'24.7104700,121.8359378',
'KP6':'24.7116865,121.8362549',
'L25':'24.7120909,121.8366787',
'KP8':'24.7113149,121.8352799',
'L26':'24.7115649,121.8354499',
'KP5':'24.710294,121.836006',
'KP10':'24.7104593,121.8357859',
'L31':'24.7092630,121.8369731',
'Kp13':'24.708954,121.836055',
'L41':'24.708976,121.837011',
'L32':'24.7093903,121.8369483',
'L12':'24.709078,121.836131',
'L2':'24.710344,121.836004',
'L33':'24.7095145,121.8369225',
'L34':'24.7095069,121.8369701',
'L7':'24.7091213,121.8361517',
'L42':'24.709528,121.836868',
'L1':'24.710627,121.835871',
'L35':'24.7096102,121.8369761',
'L13':'24.709755,121.835964',
'L3':'24.710624,121.835855',
'L19':'24.7092298,121.8361902',
'L43':'24.709662,121.836843',
'L5':'24.710657,121.835794',
'L14':'24.709741,121.835987',
'L36':'24.7096647,121.8369479',
'L8':'24.7093193,121.8362016',
'L4':'24.7108117,121.8359009',
'L15':'24.709918,121.835931',
'L37':'24.7097034,121.8368641',
'L16':'24.709935,121.835837',
'L10':'24.7109235,121.8358791',
'L44':'24.709772,121.836868',
'L38':'24.7099342,121.8369419',
'L11':'24.709830,121.835863',
'L9':'24.7108927,121.8358030',
'L22':'24.7094448,121.8361047',
'Kp22':'24.709804,121.836898',
'L27':'24.7094356,121.8361175',
'L39':'24.7100095,121.8370583',
'L18':'24.710150,121.835747',
'L29':'24.7096333,121.8361735',
'L45':'24.709834,121.836900',
'L23':'24.711191,121.835890',
'L17':'24.7111702,121.8360296',
'L40':'24.7100055,121.8368447',
'L20':'24.711219,121.835962',
'L28':'24.711115,121.836045',
'L30':'24.7100664,121.8356555',
'L46':'24.710681,121.835544',
'L47':'24.710861,121.835546',
'L48':'24.710987,121.835510',
'L49':'24.711050,121.835533',
'KP15':'24.7109366,121.8361171',
'L61':'24.7104191,121.8368058',
'L50':'24.711619,121.835123',
'L62':'24.7105751,121.8366764',
'L64':'24.7110161,121.8360699',
'L68':'24.7111836,121.8360866',
'L65':'24.7104953,121.8361815',
'L67':'24.711304,121.835752',
'L66':'24.7101429,121.8359257',
'L63':'24.7109896,121.8369664',
'L69':'24.7112884,121.8361999',
'L70':'24.711343,121.835900',
'L81':'24.711762,121.835119',
'L82':'24.711757,121.835123',
'L83':'24.7112467,121.8368239',
'L111':'24.7093830,121.8368269',
'L141':'24.709278,121.837010',
'L55':'24.710242,121.836033',
'L112':'24.7095036,121.8369671',
'L71':'24.7096723,121.8357923',
'L84':'24.7105461,121.8356880',
'L101':'24.7110295,121.8359860',
'L72':'24.7096522,121.8359126',
'L85':'24.7115065,121.8353279',
'L86':'24.7114915,121.8354489',
'L87':'24.7115692,121.8354268',
'L73':'24.7105078,121.8354654',
'L88':'24.7115933,121.8354811',
'L102':'24.7113225,121.8359689',
'L52':'24.711336,121.835839',
'L89':'24.7115403,121.8355837',
'L90':'24.7115994,121.8355244',
'KP17':'24.7106366,121.8354647',
'L51':'24.711506,121.835593',
'L91':'24.7114507,121.8355572',
'L103':'24.7115372,121.8361175',
'L142':'24.710789,121.836698',
'L53':'24.711468,121.835518',
'L113':'24.7111620,121.8366667',
'L104':'24.7115552,121.8361956',
'L74':'24.7108038,121.8357403',
'L92':'24.7110773,121.8355760',
'L54':'24.711740,121.835548',
'L105':'24.7115473,121.8362449',
'L143':'24.710794,121.836630',
'L93':'24.7114303,121.8354871',
'L114':'24.7112034,121.8364310',
'L106':'24.7115518,121.8362724',
'L56':'24.711798,121.835624',
'L107':'24.7115567,121.8363039',
'L115':'24.7112701,121.8365446',
'L94':'24.7115930,121.8355066',
'L144':'24.710914,121.836712',
'L75':'24.7112524,121.8350788',
'L95':'24.7116316,121.8353866',
'L57':'24.711848,121.835784',
'L76':'24.7111702,121.8352746',
'L108':'24.7116018,121.8362761',
'L116':'24.7113901,121.8364759',
'L145':'24.711193,121.836552',
'L58':'24.711890,121.835603',
'L149':'24.7117258,121.8370898',
'L109':'24.7116088,121.8361671',
'L59':'24.711978,121.835570',
'Kp16':'24.7117538,121.8353681',
'KP18':'24.7116989,121.8351784',
'L121':'24.7116880,121.8358995',
'L110':'24.7114964,121.8359968',
'L117':'24.7115765,121.8363676',
'L77':'24.7116073,121.8353581',
'L122':'24.7117090,121.8358409',
'L123':'24.7117163,121.8357594',
'L118':'24.7117940,121.8364527',
'L146':'24.7116283,121.8361007',
'L78':'24.7117596,121.8352860',
'L147':'24.711937,121.836174',
'L79':'24.7118829,121.8353946',
'L60':'24.711873,121.835485',
'L80':'24.7120166,121.8354992',
'L124':'24.7117650,121.8354975',
'L148':'24.711786,121.836031',
'L119':'24.7117465,121.8360075',
'L125':'24.711969,121.835727',
'L99':'24.7119207,121.8360886',
'L127':'24.7113865,121.8365657',
'L96':'24.7119996,121.8363213',
'L128':'24.7119789,121.8358479',
'L97':'24.7119545,121.8364045',
'L126':'24.711461,121.835743',
'Kp19':'24.7113137,121.8365188',
'L120':'24.7119511,121.8366274',
'L130':'24.711355,121.835619',
'L150':'24.7118628,121.8351076',
'L129':'24.7113661,121.8367635',
'L98':'24.7118150,121.8357477',
'L100':'24.7116749,121.8356565',
'Kp20':'24.7109866,121.8352598',
'L151':'24.7116374,121.8367676',
'L152':'24.7098063,121.8370180',

'L131':'24.708678,121.836171',
'L221':'24.7088490,121.8369567',
'L161':'24.7085207,121.8368306',
'L171':'24.7081013,121.8358999',
'L183':'24.7079721,121.8360538',
'L191':'24.709284,121.836628',
'L172':'24.7084848,121.8360182',
'L222':'24.7093108,121.8368920',
'L201':'24.709644,121.836124',
'L203':'24.709576,121.836092',
'L181':'24.7084921,121.8364082',
'L202':'24.709638,121.836139',
'L192':'24.7101027,121.8369805',
'L223':'24.7101517,121.8370267',
'L153':'24.710316,121.835852',
'L204':'24.710409,121.835893',
'L162':'24.710187,121.836648',
'L173':'24.7101060,121.8360209',
'L193':'24.7104374,121.8367622',
'L154':'24.710504,121.835850',
'L224':'24.7109235,121.8367823',
'L174':'24.7102544,121.8359699',
'L211':'24.710894,121.836926',
'L225':'24.7111787,121.8367900',
'L194':'24.7106369,121.8367602',
'L175':'24.7103214,121.8357366',
'L132':'24.710952,121.835737',
'L212':'24.710951,121.837072',
'L205':'24.710953,121.835961',
'L163':'24.710512,121.836561',
'L195':'24.7109363,121.8365724',
'L133':'24.710999,121.835819',
'L155':'24.710984,121.835762',
'L206':'24.710950,121.836005',
'L176':'24.7105513,121.8353212',
'L226':'24.7113831,121.8366482',
'L213':'24.711273,121.837007',
'L196':'24.7110121,121.8366757',
'L134':'24.711065,121.835912',
'L177':'24.7106622,121.8355871',
'L164':'24.710878,121.836393',
'L197':'24.7109750,121.8367900',
'L214':'24.711395,121.836930',
'L135':'24.711121,121.835771',
'L165':'24.710850,121.836554',
'L215':'24.711463,121.836887',
'L178':'24.7108772,121.8355133',
'L166':'24.711001,121.836619',
'L159':'24.711322,121.835928',
'L207':	'24.711429,121.836165',
'L179':'24.7108617,121.8353547',
'L198':'24.7111066,121.8365895',
'L180':'24.7106421,121.8353500',
'L167':'24.711075,121.836514',
'L227':'24.7119862,121.8365503',
'L156':'24.711499,121.835806',
'L209':'24.711383,121.836025',
'L168':'24.711006,121.836363',
'L157':'24.711552,121.835843',
'L228':'24.7119606,121.8365044',
'L182':'24.7112183,121.8351579',
'L216':'24.711428,121.836516',
'L136':'24.7113039,121.8356702',
'L199':'24.7114163,121.8364283',
'L185':'24.7112622,121.8353752',
'L169':'24.711113,121.836398',
'L184':'24.7112470,121.8355314',
'L217':'24.711499,121.836403',
'L200':'24.7112381,121.8364189',
'L170':'24.711228,121.836311',
'L137':'24.7114200,121.8355871',
'L186':'24.7108754,121.8359046',
'L187':'24.7108364,121.8359042',
'L218':'24.711538,121.836416',
'L138':'24.7113670,121.8355586',
'L231':'24.711269,121.836350',
'L188':'24.7108005,121.8359277',
'L229':'24.7116810,121.8361738',
'L236':'24.7115001,121.8363850',
'L208':'24.711811,121.836352',
'L232':'24.711344,121.836402',
'L219':'24.711834,121.836231',
'L158':'24.711952,121.835225',
'L139':'24.7115196,121.8355720',
'L230':'24.7116813,121.8358459',
'L189':'24.7115342,121.8348897',
'L190':'24.7115954,121.8348870',
'L220':'24.712062,121.835531',
'L233':'24.711633,121.836377',
'L140':'24.7114830,121.8354429',
'L251':'24.7116901,121.8349554',
'L241':'24.7117678,121.8358010',
'L160':'24.711868,121.834870',
'L261':'24.712055,121.835320',
'L253':'24.7117909,121.8351794',
'L252':'24.7117516,121.8352166',
'L234':'24.711809,121.836271',
'L262':'24.712074,121.835288',
'L210':'24.711920,121.836524',
'L242':'24.7114830,121.8354429',
'L255':'24.7118074,121.8352582',
'L254':'24.7118132,121.8352910',
'L244':'24.7118908,121.8362251',
'L257':'24.7117328,121.8352880',
'L256':'24.711832,121.835226',
'L258':'24.7116974,121.8353785',
'L237':'24.7119676,121.8366003',
'L259':'24.7117230,121.8354201',
'L265':'24.711781,121.834945',
'L243':'24.7116910,121.8352323',
'L260':'24.7117623,121.8354483',
'L245':'24.7117358,121.8354020',
'L266':'24.711790,121.834912',
'L250':'24.7119399,121.8353802',
'L246':'24.7120620,121.8354553',
'L263':'24.711111,121.835579',
'L235':'24.712596,121.836702',
'L264':'24.711736,121.835823',
'L248':'24.7119798,121.8361879',
'L238':'24.712047,121.836950',
'L239':'24.711810,121.836654',
'L240':'24.7116106,121.8360467',
'L249':'24.7115957,121.8359438',
'L269':'24.7115619,121.8352059',
'L268':'24.711067,121.835973',
'L267':'24.7110268,121.8359421',
'L271':'24.7110883,121.8355032',
'L270':'24.710770,121.836823',
'L272':'24.710820,121.836865',
'L273':'24.711585,121.836346',
'L275':'24.711708,121.836272',
'L311': '24.7087677,121.8369429',
'kp28': '24.7085527,121.8368222',
'KP25': '24.7079115,121.8359344',
'L368': '24.7093135,121.8367763',
'KP12': '24.7084592,121.8362325',
'L277': '24.709243,121.836788',
'L312': '24.7103756,121.8370197',
'L361': '24.7104837,121.8368467',
'L351': '24.7108062,121.8361855',
'L313': '24.7107919,121.8370170',
'l281': '24.710511,121.836563',
'KP29': '24.7097512,121.8361316',
'L278': '24.710645,121.836724',
'L352': '24.7112314,121.8363572',
'L330': '24.7112722,121.8369999',
'L362': '24.7113402,121.8367022',
'L314': '24.7114331,121.8369486',
'L353': '24.7113798,121.8363156',
'L364': '24.7113865,121.8367438',
'L315': '24.7115381,121.8369121',
'L279': '24.710539,121.836990',
'L354': '24.7114428,121.8362985',
'L270': '24.710606,121.836035',
'L365': '24.7113408,121.8366536',
'L355': '24.7114431,121.8363441',
'L282': '24.7112360,121.8365460',
'L291': '24.7112506,121.8358442',
'L282': '24.710952,121.836370',
'L317': '24.7116036,121.8370361',
'L356': '24.7114108,121.8362569',
'L363': '24.7111391,121.8363230',
'L280': '24.711245,121.836714',
'L318': '24.7116551,121.8369590',
'L319': '24.7116877,121.8369620',
'L371': '24.711340,121.836474',
'L366': '24.7114596,121.8365681',
'L357': '24.7115774,121.8362388',
'L373': '24.711363,121.836473',
'L341': '24.7114882,121.8349303',
'L369': '24.7114419,121.8364886',
'L375': '24.711367,121.836442',
'L370': '24.7115293,121.8364893',
'L283': '24.711669,121.836065',
'L358': '24.7116548,121.8361758',
'L376': '24.7115509,121.8364286',
'L372': '24.7115960,121.8365225',
'L301': '24.7119118,121.8353219',
'L316': '24.7117492,121.8355488',
'L302': '24.7120002,121.8360001',
'L381': '24.711991,121.835861',
'L247': '24.7115320,121.8346470',
'L303': '24.7113636,121.8370013',
'L304': '24.7112744,121.8369972',
'L305': '24.7111641,121.8370482',
'L331': '24.7111921,121.8358657',
'L306': '24.7107462,121.8370100',
'L332': '24.7111921,121.8358657',
'L333': '24.7109433,121.8355143',
'L374': '24.7105041,121.8363106',
'L377': '24.7102007,121.8363495',

'L307': '24.7087004,121.8370241',
'L392': '24.710620,121.836212',
'L308': '24.7102544,121.8370428',
'L284': '24.7102014,121.8357684',
'L393': '24.710696,121.836082',
'L320': '24.7103750,121.8360219',
'L321': '24.7104341,121.8364705',
'L292': '24.7104733,121.8357446',
'L334': '24.7106339,121.8360038',
'L309': '24.7109771,121.8367307',
'L293': '24.7108102,121.8356749',
'L294': '24.7109317,121.8357725',
'L322': '24.7106734,121.8367330',
'L335': '24.7108382,121.8359827',
'L295': '24.7109415,121.8357705',
'Kp31': '24.7109031,121.8360400',
'L296': '24.7110243,121.8358539',
'L394': '24.710696,121.836082',
'L336': '24.7112107,121.8357638',
'L342': '24.711500,121.836990',
'KP27': '24.7111602,121.8358070',
'L395': '24.711390,121.836105',
'L337': '24.7111663,121.8358479',
'L285': '24.7108382,121.8359113',
'L286': '24.7108382,121.8359113',
'L274': '24.711508,121.836371',
'L401': '24.711366,121.836534',
'L304': '24.7119061,121.8367790',
'L287': '24.7109131,121.8359116',
'L402': '24.711268,121.836608',
'L290': '24.7109131,121.8359116',
'L391': '24.7115320,121.8346470',
'L403': '24.711501,121.836594',
'KP11': '24.7117285,121.8356521',
'L404': '24.711431,121.836629',
'L406': '24.711608,121.836498',
'L405': '24.711582,121.836488',
'L338': '24.7118357,121.8359515',
'L339': '24.7104057,121.8359337',
'L310': '24.7108754,121.8356206',
'L407': '24.711286,121.836256',
'L408': '24.711338,121.836281',
'Kp23': '24.7026102,121.8249453',
'L288': '24.712218,121.836813',
'L297': '24.711889,121.836794',

}

CONST_GPS['新城溪'] = {
    "SN2" : "24.447769,121.805277",
}
CONST_GPS['南澳'] = {
    'Sn1': '24.4414334,121.8088263',
    'SN4': '24.4413439,121.8086275',
    'LR6': '24.443792,121.810577',
    'N10': '24.442817,121.810874',
    'N11': '24.4428161,121.8107629',
    'KP4': '24.4418231,121.8093681',
    'N20': '24.442880,121.810845',
    'N19': '24.4428219,121.8108729',
    'KP7': '24.442802,121.810840',
    'SN6': '24.4483180,121.8061937',
    'LR1': '24.4470580,121.8078694',
    'SN2': '24.4484370,121.8056875',
    'SN7': '24.4483982,121.8048563',
    'N26': '24.4459318,121.8110599',
    'N22': '24.4459873,121.8111582',
    'N29': '24.4459656,121.8111706',
    'N34': '24.4460291,121.8111367',
    'N31': '24.446024,121.811130',
    'N32': '24.4459956,121.8111039',
    'N41': '24.4459916,121.8110415',
    'N33': '24.446164,121.811033',
    'KP2': '24.4460490,121.8109583',
    'N49': '24.446082,121.811028',
    'SN10': '24.4466255,121.8098999',
    'LR2': '24.4461427,121.8106365',
    'N42': '24.4459357,121.8109218',
    'N36': '24.4459251,121.8115387',
    'LR11': '24.4459541,121.8116490',
    'N43': '24.4457813,121.8116591',
    'N45': '24.4457544,121.8116631',
    'SN8': '24.4426454,121.8098684',
    'N1': '24.4457508,121.8117630',
    'N5': '24.445747,121.811704',
    'N4': '24.4457947,121.8116728',
    'N3': '24.4457154,121.8116494',
    'N15': '24.445593,121.811317',
    'N7': '24.4457999,121.8116269',
    'N13': '24.4457532,121.8116289',
    'N17': '24.445743,121.811662',
    'N6': '24.445655,121.811519',
    'N9': '24.4457886,121.8115240',
    'N35': '24.445841,121.811497',
    'N16': '24.4458658,121.8112400',
    'N24': '24.445710,121.811267',
    'N44': '24.445990,121.811378',
    'N25': '24.4458701,121.8112041',
    'N12': '24.4460093,121.8113550',
    'N28': '24.4459052,121.8111873',
    'N27': '24.445886,121.811142',
    'N46': '24.4459403,121.8112189',
    'N14': '24.445972,121.811248',
    'N18': '24.4459660,121.8111843',
    'N30': '24.445880,121.811165',
    'N23': '24.4460282,121.8111602',
    'XXX': '24.4459714,121.8111521',
    'N51': '24.4459196,121.8110861',
    'XXX': '24.4459934,121.8111149',
    'N52': '24.445873,121.811122',
    'LR8': '24.4460316,121.8111692',
    'N61': '24.4460706,121.8111327',
    'N63': '24.4458784,121.8105553',
    'N64': '24.4459415,121.8107139',
    'N47': '24.445975,121.810636',
    'N21': '24.4460026,121.8105795',
    'N55': '24.445804,121.810810',
    'N58': '24.4457901,121.8108246',
    'N65': '24.4458121,121.8112252',
    'N57': '24.4459077,121.8106650',
    'N48': '24.4457929,121.8109272',
    'N53': '24.446076,121.810257',
    'N54': '24.4458426,121.8109855',
    'N69': '24.4458115,121.8110147',
    'N68': '24.4457065,121.8115256',
    'N8': '24.446103,121.810262',
    'N60': '24.4458903,121.8110438',
    'N50': '24.445878,121.810300',
    'N82': '24.4458207,121.8116953',
    'N81': '24.4458277,121.8110224',
    'N84': '24.4459220,121.8111887',
    'N83': '24.4457520,121.8118207',
    'N62': '24.4455744,121.8111816',
    'N100': '24.4457328,121.8117627',
    'N72': '24.445836,121.811715',
    'SN11': '24.4485814,121.8043507',
    'N39': '24.4456073,121.8109453',
    'KP6': '24.4458402,121.8117546',
    'N71': '24.445788,121.811633',
    'N56': '24.4459736,121.8106247',
    'N88': '24.4456552,121.8117573',
    'N67': '24.445641,121.811684',
    'N59': '24.4459211,121.8109188',
    'N94': '24.4456534,121.8118740',
    'N66': '24.4459772,121.8107327',
    'N74': '24.4459660,121.8108930',
    'N91': '24.4456955,121.8120359',
    'N73': '24.445750,121.811578',
    'N77': '24.4460200,121.8110341',
    'KP3': '24.4458988,121.8115451',
    'N76': '24.4458768,121.8115756',
    'N70': '24.445841,121.811225',
    'N75': '24.4457810,121.8110663',
    'N97': '24.4458652,121.8113892',
    'N85': '24.445870,121.811360',
    'N89': '24.4458295,121.8108410',
    'N80': '24.4459333,121.8109483',
    'N115': '24.4457709,121.8111558',
    'N86': '24.4458933,121.8114318',
    'N92': '24.4458454,121.8108326',
    'N93': '24.4460020,121.8110834',
    'N87': '24.4460020,121.8110834',
    'N79': '24.445919,121.811137',
    'N101': '24.4457755,121.8105684',
    'N98': '24.4458106,121.8105678',
    'N109': '24.4457911,121.8111089',
    'N104': '24.4457203,121.8108497',
    'N107': '24.4453610,121.8105778',
    'N78': '24.4458964,121.8109530',
    'N103': '24.446017,121.811128',
    'N110': '24.4455704,121.8106432',
    'N102': '24.4459064,121.8112172',
    'N113': '24.4458158,121.8106931',
    'KP5': '24.4411611,121.8086215',
    'SN12': '24.447303,121.806863',
    'LR7': '24.4469900,121.8079137',
    'SN3': '24.447291,121.807586',

    'N90': '24.4458335, 121.8113533',
    'N99': '24.445895,121.811465',
    'N112': '24.4456555, 121.8112564',
    'N116': '24.4456934, 121.8112926',
    'N120': '24.4456934, 121.8113875',
    'N114': '24.4458832, 121.8109795',
    'N194': '24.445772,121.810819',
    'N106': '24.4459428, 121.8107934',
    'N196': '24.445657,121.810895',
    'N118': '24.4460645, 121.8106013',
    'N105': '24.4456818, 121.8109047',
    'N122': '24.4459223, 121.8105064',
    'N37': '24.4456037, 121.8105292',
    'N117': '24.4455765, 121.8106724',
    'N198': '24.445992,121.810379',
    'N121': '24.4459992, 121.8109248',
    'N96': '24.4459690, 121.8105020',
    'N119': '24.4457395, 121.8103887',
    'N108': '24.4460706, 121.8106838',
    'N126': '24.4458600, 121.8111129',
    'N125': '24.4458304, 121.8112936',
    'N124': '24.4459702, 121.8108095',
    'N127': '24.445909,121.811367',
    'N129': '24.4459125, 121.8110918',
    'N130': '24.4459476, 121.8111753',
    'N132': '24.445833,121.811249',
    'KP8': '24.4413656, 121.8090094',
    'SN9': '24.4411843, 121.8094979',

}

CONST_GPS['和平'] = {
    "SN4" : "24.446823,121.807661",
}

for zone in CONST_GPS.keys():
    new_data = {}
    for nest in CONST_GPS[zone].keys():
        new_data[nest.upper()] = CONST_GPS[zone][nest]
    CONST_GPS[zone] = new_data


# 2024 notes
"""
於 0606 整理蘭陽0602紀錄之異動
1. 移除重複的 L202, L132, L185, L208, L139, L251, L270, L282, L291, L247,
2. 補上缺少的 L367 資料
3. L304 是 0602 記錄新巢, 前一次調查 0525 時 L213 誤收旗之後被插L304旗, 並且在隔周該巢被紀錄為成功 已修正 L213 資料與 L304 資料
4. L202 2雛成功收旗是誤判, 修正為 2雛一蛋, 但已收旗
"""

