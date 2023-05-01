from hypixel.api import HypixelAPI

class Tasks():
    def __init__(self, api_instance: HypixelAPI) -> None:
        self.api = api_instance
        self.auctions = []

    async def scheduled_task(self):
        """"""
        self.auctions = await self.api.get_all_auctions()

    def get_auctions(self):
        return self.auctions