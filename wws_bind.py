from typing import List
import httpx
import traceback
import json
import re
from pathlib import Path

from requests import head

from .data_source import servers
from .wws_info import get_AccountIdByName
from .utils import match_keywords
dir_path = Path(__file__).parent
cfgpath = dir_path / 'config.json'
config = json.load(open(cfgpath, 'r', encoding='utf8'))
headers = {
    'Authorization': config['token']
}

async def get_BindInfo(user,info):
    try:
        if isinstance(info,List) and len(info) == 1:
            for i in info:              #是否包含me或@
                if i == 'me':
                    url = 'https://api.wows.linxun.link/public/wows/bind/account/platform/bind/list'
                    params = {
                    "platformType": "QQ",
                    "platformId": user,
                    }
                match = re.search(r"CQ:at,qq=(\d+)",i)
                if match:
                    url = 'https://api.wows.linxun.link/public/wows/bind/account/platform/bind/list'
                    params = {
                    "platformType": "QQ",
                    "platformId": match.group(1),
                    }
                    break
        else:
            return '参数似乎出了问题呢，请使用me或@群友'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            result = resp.json()
        if result['code'] == 200 and result['message'] == "success":
            if result['data']:
                msg1 = f'当前绑定账号\n'
                msg2 = f'绑定账号列表\n'
                flag = 1
                for bindinfo in result['data']:
                    msg2 += f"{flag}：{bindinfo['serverType']} {bindinfo['userName']}\n"
                    flag += 1
                    if bindinfo['defaultId']:
                        msg1 += f"{bindinfo['serverType']} {bindinfo['userName']}\n"
                msg = msg1+msg2+"本人发送[wws 切换绑定+序号] 切换对应账号"
                return msg
            else:
                return '该用户似乎还没绑定窝窝屎账号'
        else:
            return result['message']
    except Exception:
        traceback.print_exc()
        return 'wuwuwu出了点问题，请联系麻麻解决'
    
async def set_BindInfo(user,info):
    try:
        param_server = None
        if isinstance (info,List):
            if len(info) == 2:
                param_server,info = await match_keywords(info,servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(param_server,str(info[0]))
                    if param_accountid:
                        url = 'https://api.wows.linxun.link/api/wows/bind/account/platform/bind/put'
                        params = {
                        "platformType": "QQ",
                        "platformId": str(user),
                        "accountId": param_accountid
                        }
                    else:
                        return '无法查询该游戏昵称Orz，请检查昵称是否存在'
                else:
                    return '服务器参数似乎输错了呢'
            else:
                return '参数似乎输错了呢，请确保后面跟随服务器+游戏昵称'
        else:
            return '参数似乎输错了呢，请确保后面跟随服务器+游戏昵称'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            result = resp.json()
        if result['code'] == 200 and result['message'] == "success":
            return '绑定成功'
        elif result['code'] == 500:
            return result['message']
        else:
            return 'wuwuwu出了点问题，请联系麻麻解决'
    except Exception:
        traceback.print_exc()
        return 'wuwuwu出了点问题，请联系麻麻解决'

async def change_BindInfo(user,info):
    try:
        if isinstance(info,List) and len(info) == 1 and str(info[0]).isdigit:
            url = 'https://api.wows.linxun.link/public/wows/bind/account/platform/bind/list'
            params = {
            "platformType": "QQ",
            "platformId": user,
            }
        else:
            return '参数似乎出了问题呢，请跟随要切换的序号'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            result = resp.json()
        if result['code'] == 200 and result['message'] == "success":
            if result['data'] and len(result['data']) >= int(info[0]):
                account_name = result['data'][int(info[0])-1]['userName']
                param_server = result['data'][int(info[0])-1]['serverType']
                param_accountid = await get_AccountIdByName(param_server,account_name)
                if param_accountid:
                    url = 'https://api.wows.linxun.link/api/wows/bind/account/platform/bind/put'
                    params = {
                    "platformType": "QQ",
                    "platformId": str(user),
                    "accountId": param_accountid
                    }
                else:
                    return '无法查询该游戏昵称Orz，请检查昵称是否存在'
            else:
                return '没有对应序号的绑定记录'
        else:
            return '参数似乎不正确，请确保只跟随了序号'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            result = resp.json()
        if result['code'] == 200 and result['message'] == "success":
            return f'切换绑定成功,当前绑定账号{account_name}'
        elif result['code'] == 500:
            return result['message']
        else:
            return 'wuwuwu出了点问题，请联系麻麻解决'
    except Exception:
        traceback.print_exc()
        return 'wuwuwu出了点问题，请联系麻麻解决'