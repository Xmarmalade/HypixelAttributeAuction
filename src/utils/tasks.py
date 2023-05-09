import time
from hypixel.api import HypixelAPI

class Tasks():
    update_time = 0

    def __init__(self, api_instance: HypixelAPI) -> None:
        self.api = api_instance
        self.auctions = []

    async def scheduled_task(self):
        """"""
        self.auctions = await self.api.get_all_auctions()
        Tasks.update_time = int(time.time())

    def get_auctions(self):
        return self.auctions
    
    @classmethod
    def get_update_time(cls):
        return cls.update_time