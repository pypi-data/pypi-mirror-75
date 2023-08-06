from typing import *
import royalnet
import royalnet.commands as rc
import datetime


class PongEvent(rc.Event):
    name = "pong"

    async def run(self, **kwargs) -> dict:
        return {"timestamp": datetime.datetime.now().timestamp()}
