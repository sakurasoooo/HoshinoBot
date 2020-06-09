import pytz
from datetime import datetime
from hoshino import util
from hoshino.service import Service
from hoshino.res import R
sv = Service('manacall', enable_on_default=True)

# def get_hour_call():
#     """从HOUR_CALLS中挑出一组时报，每日更换，一日之内保持相同"""
#     config = util.load_config(__file__)
#     now = datetime.now(pytz.timezone('Asia/Shanghai'))
#     hc_groups = config["HOUR_CALLS"]
#     g = hc_groups[ now.day % len(hc_groups) ]
#     return config[g]

@sv.scheduled_job('cron', hour='*')
async def mana_call():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour%6!=0:
        return 
    pic = R.img('mana小助手.png').cqcode
    msg = f"{pic}"
    await sv.broadcast(msg, 'manacall', 0)
