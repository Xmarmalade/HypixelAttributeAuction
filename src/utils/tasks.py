import time
from hypixel.api import HypixelAPI
from .timeholder import Timeholder

class Tasks():
    update_time = 0

    def __init__(self, api_instance: HypixelAPI) -> None:
        self.api = api_instance
        self.auctions = []

    async def scheduled_task(self):
        self.auctions = await self.api.get_all_auctions()
        Timeholder.update_time = int(time.time())

    def get_auctions(self):
        return self.auctions
    