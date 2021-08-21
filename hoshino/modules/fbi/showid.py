import time
from hoshino.service import Service
from hoshino.typing import HoshinoBot, CQEvent
from .Kyaru_Head.Kyaru_Head import add_head
from .showmyid.show_id import add_head as add_id , add_grouphead as add_groupid


sv = Service('接头霸王')

@sv.on_prefix(('接头霸王', '接头'))
async def concat_head(bot: HoshinoBot, ev: CQEvent):
    #uid = ev.user_id
    msg = await add_head(str(ev.message))
    await bot.send(ev, msg)

@sv.on_prefix(('出示证件', '出示'))
async def concat_id(bot: HoshinoBot, ev: CQEvent):
    msg = "没找到头"
    # if(len(ev.message)!=2):
    #     await bot.send(ev, msg)
    #     return
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            uid = m.data['qq']
            msg = await add_groupid(uid)
            break
        if(m.type == 'image'):
            msg = await add_id(str(ev.message))
            break
    print(msg)
    await bot.send(ev, msg)

