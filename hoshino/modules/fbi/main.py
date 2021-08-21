import time
from hoshino.service import Service
from hoshino.typing import HoshinoBot, CQEvent
from .Kyaru_Head.Kyaru_Head import add_head
from .showmyid.show_id import add_head as add_id

# async def main():
#     await add_head("https://c2cpicdw.qpic.cn/offpic_new/1010704939//1010704939-3384525135-1533A3DEEEAF98044E13AA90024C0153/0?term=3")
#     print("END")
sv = Service('接头霸王')

@sv.on_prefix(('接头霸王', '接头'))
async def concat_head(bot: HoshinoBot, ev: CQEvent):
    #uid = ev.user_id
    msg = await add_head(str(ev.message))
    await bot.send(ev, msg)

@sv.on_prefix(('出示证件', '出示'))
async def concat_head(bot: HoshinoBot, ev: CQEvent):

    msg = await add_id(str(ev.message))
    await bot.send(ev, msg)