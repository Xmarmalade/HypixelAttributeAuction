from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every

from operator import itemgetter

from typing import Union

from hypixel.api import HypixelAPI
from utils.tasks import Tasks
from utils.itemutil import ItemUtil

from models.response import AuctionData, AuctionResponse, MultipleAuctionResponse, EmptyResponse

app = FastAPI()
api = HypixelAPI()
tasks = Tasks(api_instance=api)

@app.on_event('startup')
@repeat_every(seconds=15 * 60)
async def update_auctions():
    await tasks.scheduled_task()

@app.get('/')
def get_root():
    return 'Why are you here?'
    
@app.get('/api/auction/auction_id/{auction_id}', response_model=AuctionResponse)
async def get_auction_id(auction_id: str):
    try:
        res = await api.get_auction_by_auction_id(auction_id=auction_id)
        return res
    except HTTPException as e:
        raise e

@app.get('/api/auction/uuid/{uuid}', response_model=Union[MultipleAuctionResponse, EmptyResponse])
async def get_auction_uuid(uuid: str):
    try:
        res = await api.get_active_auction_by_uuid(uuid=uuid)
        return res
    except HTTPException as e:
        raise e

@app.get('/api/auction/profile_id/{profile_id}', response_model=Union[MultipleAuctionResponse, EmptyResponse])
async def get_auction_uuid(profile_id: str):
    res = await api.get_active_auction_by_profileid(profile_id=profile_id)
    return res

@app.get('/api/auctions')
async def get_all_auctions() -> MultipleAuctionResponse:
    res = tasks.get_auctions()
    return {
        'success': True,
        'data': res
    }

@app.get('/api/auction/item_id/{item_id}', response_model=Union[MultipleAuctionResponse, EmptyResponse])
async def get_auction_item_id(item_id: str, attribute1: str = '', attribute2: str = ''):
    all_auctions = tasks.get_auctions()
    auctions: list[AuctionData] = []
    for auction in all_auctions:
        if auction['item_id'] == item_id:
            if ItemUtil.check_attribute(auction_data=auction, attribute1=attribute1, attribute2=attribute2):
                auctions.append(auction.copy())
    auctions = sorted(auctions, key=itemgetter('price'))
    return {
        'success': True,
        'data': auctions
    }

@app.get('/api/debug')
async def debug_endpoint():
    res = await api.debug_func()
    return {'data': res}