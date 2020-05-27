import random
import json
from hoshino import aiorequests
from nonebot import NoneBot
from hoshino import util
from hoshino.service import Service, Privilege

sv = Service('deepchat', manage_priv=Privilege.SUPERUSER, enable_on_default=False, visible=False)

# api = util.load_config(__file__)['deepchat_api']

# @sv.on_message('group')
# async def deepchat(bot:NoneBot, ctx):
#     msg = ctx['message'].extract_plain_text()
#     if not msg or random.random() < 0.025:
#         return
#     payload = {
#         "msg": msg,
#         "group": ctx['group_id'],
#         "qq": ctx['user_id']
#     }
    # sv.logger.info(payload)
#     rsp = await aiorequests.post(api, data=payload)
#     j = await rsp.json()
#     sv.logger.info(j)
#     if j['msg']:
#         await bot.send(ctx, j['msg'])
key = util.load_config(__file__)['deepchat_api']
api = "http://openapi.tuling123.com/openapi/api/v2"
@sv.on_message('group')
async def deepchat(bot:NoneBot, ctx):
    msg = ctx['message'].extract_plain_text()
    if not msg or random.random() > 0.05:
        return
    req = {
        "reqType":0,
        "perception": {
            "inputText": {
                "text": msg
            }
        },
        "userInfo": {
            "apiKey": key,
            "userId": f"{ctx['user_id']}"
        }
        # "msg": msg,
        # "group": ctx['group_id'],
        # "qq": ctx['user_id']
    }

    sv.logger.info(req)
    req = json.dumps(req).encode('utf8') 
    rsp = await aiorequests.post(api, data=req)
    rsp= await rsp.json()
    
    # rsp = await json.loads(rsp)
    j =  rsp["results"][0]["values"]["text"]
    sv.logger.info(j)
    if rsp["intent"]["code"] < 4000 or rsp["intent"]["code"]>10000 :
        await bot.send(ctx, j)
    else:
        await bot.send(ctx, f"我的头有点晕@_@")