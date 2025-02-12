from dataclasses import dataclass
from re import L
from typing import Tuple,List
import time
import traceback

@dataclass
class matching:
    keywords: Tuple[str, ...]
    match_keywords : str
    
command_list = [
    matching(("切换绑定","更换绑定","更改绑定"),"changebind"),
    matching(("查询绑定","绑定查询","绑定列表","查绑定"),"bindlist"),
    matching(("bind","绑定","set"),"bind"),
    matching(("recent","近期",),"recent"),
    matching(("ship","单船",),"ship"),
    matching(("搜船名","查船名","船名"),"searchship"),
]

nations = [
    matching(("commonwealth","英联邦",),"commonwealth"),
    matching(("europe","欧洲",),"europe"),
    matching(("france","法国",),"france"),
    matching(("germany","德国",),"germany:"),
    matching(("italy","意大利",),"italy"),
    matching(("japan","日本",),"japan"),
    matching(("pan_america","泛美",),"pan_america"),
    matching(("pan_asia","泛亚",),"pan_asia"),
    matching(("uk","英国","United_Kingdom"),"United_Kingdom"),
    matching(("usa","美国",),"usa"),
    matching(("ussr","苏联",),"ussr"),
    matching(("netherlands","荷兰",),"netherlands"),
    matching(("spain","西班牙",),"spain"),
]

shiptypes = [
    matching(("Cruiser","巡洋舰","巡洋","CA"),"Cruiser"),
    matching(("Battleship","战列舰","战列","BB"),"Battleship"),
    matching(("Destroyer","驱逐舰","驱逐","DD"),"Destroyer"),
    matching(("Submarine","潜艇","SS"),"Submarine"),
    matching(("Auxiliary","辅助舰艇","DD"),"Auxiliary"),
    matching(("AirCarrier","航空母舰","航母","CV"),"AirCarrier"),
]

levels = [
    matching(("1","1级","一级","一"),"1"),
    matching(("2","2级","二级","二"),"2"),
    matching(("3","3级","三级","三"),"3"),
    matching(("4","4级","四级","四"),"4"),
    matching(("4","4级","四级","四"),"4"),
    matching(("5","5级","五级","五"),"5"),
    matching(("6","6级","六级","六"),"6"),
    matching(("7","7级","七级","七"),"7"),
    matching(("8","8级","八级","八"),"8"),
    matching(("9","9级","九级","九"),"9"),
    matching(("10","10级","十级","十"),"10"),
    matching(("11","11级","十一级","十一"),"11"),
]

servers = [
    matching(("asia","亚服","asian"),"asia"),
    matching(("eu","欧服","europe"),"eu"),
    matching(("na","美服","NorthAmerican"),"na"),
    matching(("ru","俄服","Russia"),"ru"),
    matching(("cn","国服","china"),"cn"),
]

pr_select = [
    {
        "value": 0,
        "name": "还需努力",
        "englishName": "Bad",
        "color": "#FE0E00"
    },
    {
        "value": 750,
        "name": "低于平均",
        "englishName": "Below Average",
        "color": "#FE7903"
    },
    {
        "value": 1100,
        "name": "平均水平",
        "englishName": "Average",
        "color": "#FFC71F"
    },
    {
        "value": 1350,
        "name": "好",
        "englishName": "Good",
        "color": "#44B300"
    },
    {
        "value": 1550,
        "name": "很好",
        "englishName": "Very Good",
        "color": "#318000"
    },
    {
        "value": 1750,
        "name": "非常好",
        "englishName": "Great",
        "color": "#02C9B3"
    },
    {
        "value": 2100,
        "name": "大佬水平",
        "englishName": "Unicum",
        "color": "#D042F3"
    },
    {
        "value": 2450,
        "name": "神佬水平",
        "englishName": "Super Unicum",
        "color": "#A00DC5"
    }
]

color_data = {
    "Bad": "#FE0E00",
    "Below Average": "#FE7903",
    "Average": "#FFC71F",
    "Good": "#44B300",
    "Very Good": "#318000",
    "Great": "#02C9B3",
    "Unicum": "#D042F3",
    "Super Unicum": "#A00DC5"
}

async def set_infoparams(List):
    try:
        winsColor = await set_winColor(int(List['pvp']['wins']))
        damageColor = await set_damageColor(None,int(List['pvp']['damage']))
        bb_winsColor = await set_winColor(int(List['type']['Battleship']['wins']))
        ca_winsColor = await set_winColor(int(List['type']['Cruiser']['wins']))
        dd_winsColor = await set_winColor(int(List['type']['Destroyer']['wins']))
        cv_winsColor = await set_winColor(int(List['type']['AirCarrier']['wins']))
        bb_damageColor = await set_damageColor(None,int(List['type']['Battleship']['damage']))
        ca_damageColor = await set_damageColor('Cruiser',int(List['type']['Cruiser']['damage']))
        dd_damageColor = await set_damageColor('Destroyer',int(List['type']['Destroyer']['damage']))
        cv_damageColor = await set_damageColor('AirCarrier',int(List['type']['AirCarrier']['damage']))
        solo_winsColor = await set_winColor(int(List['pvpSolo']['wins']))
        solo_damageColor = await set_damageColor(None,int(List['pvpSolo']['damage']))
        div2_winsColor = await set_winColor(int(List['pvpTwo']['wins']))
        div2_damageColor = await set_damageColor(None,int(List['pvpTwo']['damage']))
        div3_winsColor = await set_winColor(int(List['pvpThree']['wins']))
        div3_damageColor = await set_damageColor(None,int(List['pvpThree']['damage']))
        result = {
            "guild":List['clanInfo']['tag'],
            "userName":List['userName'],
            "karma":List['karma'],
            "serverName":List['serverName'],
            "newDamage":List['dwpDataVO']['damage'],
            "newWins":round(List['dwpDataVO']['wins'],2),
            "newPr":List['dwpDataVO']['pr'],
            "prValue":f"{List['pr']['value']} {List['pr']['name']}",
            "time":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(List['lastDateTime'])),
            "battles":List['pvp']['battles'],
            "wins":List['pvp']['wins'],
            "damage":List['pvp']['damage'],
            "xp":List['pvp']['xp'],
            "kd":List['pvp']['kd'],
            "hit":List['pvp']['hit'],
            "bb_battles":List['type']['Battleship']['battles'],
            "bb_pr":List['type']['Battleship']['pr']['value'],
            "bb_wins":List['type']['Battleship']['wins'],
            "bb_damage":List['type']['Battleship']['damage'],
            "bb_hit":List['type']['Battleship']['hit'],
            "ca_battles":List['type']['Cruiser']['battles'],
            "ca_pr":List['type']['Cruiser']['pr']['value'],
            "ca_wins":List['type']['Cruiser']['wins'],
            "ca_damage":List['type']['Cruiser']['damage'],
            "ca_hit":List['type']['Cruiser']['hit'],
            "dd_battles":List['type']['Destroyer']['battles'],
            "dd_pr":List['type']['Destroyer']['pr']['value'],
            "dd_wins":List['type']['Destroyer']['wins'],
            "dd_damage":List['type']['Destroyer']['damage'],
            "dd_hit":List['type']['Destroyer']['hit'], 
            "cv_battles":List['type']['AirCarrier']['battles'],
            "cv_pr":List['type']['AirCarrier']['pr']['value'],
            "cv_wins":List['type']['AirCarrier']['wins'],
            "cv_damage":List['type']['AirCarrier']['damage'],
            "cv_hit":List['type']['AirCarrier']['hit'],      
            "solo_battles":List['pvpSolo']['battles'],
            "solo_wins":List['pvpSolo']['wins'],
            "solo_xp":List['pvpSolo']['xp'],
            "solo_damage":List['pvpSolo']['damage'],
            "solo_kd":List['pvpSolo']['kd'],
            "solo_hit":List['pvpSolo']['hit'],
            "div2_battles":List['pvpTwo']['battles'],
            "div2_wins":List['pvpTwo']['wins'],
            "div2_xp":List['pvpTwo']['xp'],
            "div2_damage":List['pvpTwo']['damage'],
            "div2_kd":List['pvpTwo']['kd'],
            "div2_hit":List['pvpTwo']['hit'],
            "div3_battles":List['pvpThree']['battles'],
            "div3_wins":List['pvpThree']['wins'],
            "div3_xp":List['pvpThree']['xp'],
            "div3_damage":List['pvpThree']['damage'],
            "div3_kd":List['pvpThree']['kd'],
            "div3_hit":List['pvpThree']['hit'],
            "lv1":List['battleCountAll']['1'],
            "lv2":List['battleCountAll']['2'],
            "lv3":List['battleCountAll']['3'],
            "lv4":List['battleCountAll']['4'],
            "lv5":List['battleCountAll']['5'],
            "lv6":List['battleCountAll']['6'],
            "lv7":List['battleCountAll']['7'],
            "lv8":List['battleCountAll']['8'],
            "lv9":List['battleCountAll']['9'],
            "lv10":List['battleCountAll']['10'],
            "newDamageColor":None,
            "newWinsColor":None,
            "newPrColor":None,
            "prValueColor":List['pr']['color'],
            "winsColor":winsColor,
            "damageColor":damageColor,
            "bb_prColor":List['type']['Battleship']['pr']['color'],
            "ca_prColor":List['type']['Cruiser']['pr']['color'],
            "dd_prColor":List['type']['Destroyer']['pr']['color'],
            "cv_prColor":List['type']['AirCarrier']['pr']['color'],
            "bb_winsColor":bb_winsColor,
            "ca_winsColor":ca_winsColor,
            "dd_winsColor":dd_winsColor,
            "cv_winsColor":cv_winsColor,
            "bb_damageColor":bb_damageColor,
            "ca_damageColor":ca_damageColor,
            "dd_damageColor":dd_damageColor,
            "cv_damageColor":cv_damageColor,
            "solo_winsColor":solo_winsColor,
            "solo_damageColor":solo_damageColor,
            "div2_winsColor":div2_winsColor,
            "div2_damageColor":div2_damageColor,
            "div3_winsColor":div3_winsColor,
            "div3_damageColor":div3_damageColor
        }
        return result
    except Exception:
        traceback.print_exc()

async def set_recentparams(List):
    try:   
        historyData = await set_historyData(List['recentList'])
        winsColor = await set_winColor(int(List['data']['wins']))
        damageColor = await set_damageColor(None,int(List['data']['damage']))
        result = {
            "guild":List['clanInfo']['tag'],
            "userName":List['userName'],
            "serverName":List['serverName'],
            "prValue":f"{List['data']['pr']['value']} {List['data']['pr']['name']}",
            "reTime":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(List['recordTime'])),
            "battles":List['data']['battles'],
            "wins":List['data']['wins'],
            "damage":List['data']['damage'],
            "xp":List['data']['xp'],
            "kd":List['data']['kd'],
            "hit":List['data']['hit'],
            "historyData":historyData,
            "prValueColor":List['data']['pr']['color'],
            "winsColor":winsColor,
            "damageColor":damageColor
        }
        return result
    except Exception:
        traceback.print_exc()
        
async def set_shipparams(List):
    try:   
        result = {
            "shipNameEn":List['shipInfo']['shipInfo']['nameEnglish'],
            "shipNameCn":List['shipInfo']['shipInfo']['nameCn'],
            "damageTop":List['dwpDataVO']['damage'],
            "winsTop":List['dwpDataVO']['wins'],
            "prTop":List['dwpDataVO']['pr'],
            "prValue":f"{List['shipInfo']['pr']['value']} {List['shipInfo']['pr']['name']}",
            "lastTime":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(List['shipInfo']['lastBattlesTime'])),
            "battles":List['shipInfo']['battles'],
            "wins":List['shipInfo']['wins'],
            "damage":List['shipInfo']['damage'],
            "xp":List['shipInfo']['xp'],
            "kda":List['shipInfo']['kd'],
            "hit":List['shipInfo']['hit'],
            "maxDamage":List['shipInfo']['extensionDataInfo']['maxDamage'],
            "maxDamageScouting":List['shipInfo']['extensionDataInfo']['maxDamageScouting'],
            "maxTotalAgro":List['shipInfo']['extensionDataInfo']['maxTotalAgro'],
            "maxXp":List['shipInfo']['extensionDataInfo']['maxXp'],
            "maxFragsBattle":List['shipInfo']['extensionDataInfo']['maxFrags'],
            "maxPlanesKilled":List['shipInfo']['extensionDataInfo']['maxPlanesKilled'],
            "prColor":List['shipInfo']['pr']['color'],
            "damageTopColor":None,
            "winsTopColor":None,
            "prTopColor":None
        }
        return result
    except Exception:
        traceback.print_exc()


async def select_prvalue_and_color(pr:int):
    for select in pr_select :
        if pr > select['value']:
            describe = select['name']
            color = select['color']
    return describe,color

async def set_historyData(List):
    historyData = ''
    for ship in List:
        historyData += r'<tr>'
        historyData += r'<td class="blueColor">'+f"{ship['shipInfo']['nameCn']}"+r'</td>'
        historyData += r'<td class="blueColor">'+f"{ship['shipInfo']['level']}"+r'</td>'
        historyData += r'<td class="blueColor">'+f"{ship['battles']}"+r'</td>'
        historyData += f'''<td class="blueColor" style="color: {ship['pr']['color']}">{ship['pr']['value']} {ship['pr']['name']}</td>'''
        historyData += r'<td class="blueColor">'+f"{ship['xp']}"+r'</td>'
        wincolor = await set_winColor(int(ship['wins']))
        historyData += f'''<td class="blueColor" style="color: {wincolor}">{ship['wins']}%</td>'''
        damagecolor = await set_damageColor(ship['shipInfo']['shipType'],int(ship['damage']))
        historyData += f'''<td class="blueColor" style="color: {damagecolor}">{ship['damage']}</td>'''
        historyData += r'<td class="blueColor">'+f"{ship['hit']}%"+r'</td>'
        historyData += r'</tr>'
    return historyData

async def set_damageColor(type:str,value:int):
    if type == 'Destroyer':
        if value < 33000:
            return color_data["Bad"]
        elif value < 40000:
            return color_data["Good"]
        elif value < 55000:
            return color_data["Great"]
        elif value < 64000:
            return color_data["Unicum"]
        else:
            return color_data["Super Unicum"]
    elif type == 'Cruiser':
        if value < 47000:
            return color_data["Bad"]
        elif value < 55000:
            return color_data["Good"]
        elif value < 83000:
            return color_data["Great"]
        elif value < 95000:
            return color_data["Unicum"]
        else:
            return color_data["Super Unicum"]
    elif type == 'AirCarrier':
        if value < 60000:
            return color_data["Bad"]
        elif value < 71000:
            return color_data["Good"]
        elif value < 84000:
            return color_data["Great"]
        elif value < 113000:
            return color_data["Unicum"]
        else:
            return color_data["Super Unicum"]
    else:
        if value < 64000:
            return color_data["Bad"]
        elif value < 72000:
            return color_data["Good"]
        elif value < 97000:
            return color_data["Great"]
        elif value < 108000:
            return color_data["Unicum"]
        else:
            return color_data["Super Unicum"]
    return None

async def set_winColor(value:int):
    if value < 45:
        return color_data["Bad"]
    elif value < 50:
        return color_data["Below Average"]
    elif value < 55:
        return color_data["Average"]
    elif value < 60:
        return color_data["Good"]
    elif value < 65:
        return color_data["Great"]
    elif value < 70:
        return color_data["Unicum"]
    else:
        return color_data["Super Unicum"]
    return None