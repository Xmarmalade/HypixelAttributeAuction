from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every

from operator import itemgetter

from typing import Union

from hypixel.api import HypixelAPI
from utils.tasks import Tasks
from utils.itemutil import ItemUtil
from utils.timeholder import Timeholder
from constant.kuudra_items import kuudra_items, kuudra_helmet, kuudra_chestplate, kuudra_leggings, kuudra_boots

from models.response import AuctionData, LowestBinData, AuctionResponse, MultipleAuctionResponse, LowestBinResponse, EmptyResponse

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
        'last_update': Timeholder.get_time(),
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
        'last_update': Timeholder.get_time(),
        'data': auctions
    }

@app.get('/api/auction/kuudra/lowestbin', response_model=Union[LowestBinResponse, EmptyResponse])
async def get_kuudra_lowestbin():
    all_auctions: list[AuctionData] = sorted(tasks.get_auctions(), key=itemgetter('price'))
    kuudra_lb_data: list[LowestBinData] = []
    for kuudra_item in kuudra_items:
        for auction in all_auctions:
            if kuudra_item in auction['item_name'] and auction['bin'] == True:
                kuudra_lb_data.append({'item_name': kuudra_item, 'data': auction})
                break
    return {
        'success': True,
        'last_update': Timeholder.get_time(),
        'data': kuudra_lb_data
    }

@app.get('/api/auction/kuudra/armor/{armor_type}', response_model=Union[MultipleAuctionResponse, EmptyResponse])
async def get_lowest_attribute_armor(armor_type: str, attribute: str = ''):
    all_auctions: list[AuctionData] = sorted(tasks.get_auctions(), key=itemgetter('price'))
    items: list[AuctionData] = []
    if armor_type == 'helmet':
        for auction in all_auctions:
            if auction['item_id'] in kuudra_helmet and auction['bin'] == True:
                if ItemUtil.check_attribute(auction_data=auction, attribute1=attribute):
                    items.append(auction.copy())
    elif armor_type == 'chestplate':
        for auction in all_auctions:
            if auction['item_id'] in kuudra_chestplate and auction['bin'] == True:
                if ItemUtil.check_attribute(auction_data=auction, attribute1=attribute):
                    items.append(auction.copy())
    elif armor_type == 'leggings':
        for auction in all_auctions:
            if auction['item_id'] in kuudra_leggings and auction['bin'] == True:
                if ItemUtil.check_attribute(auction_data=auction, attribute1=attribute):
                    items.append(auction.copy())
    elif armor_type == 'boots':
        for auction in all_auctions:
            if auction['item_id'] in kuudra_boots and auction['bin'] == True:
                if ItemUtil.check_attribute(auction_data=auction, attribute1=attribute):
                    items.append(auction.copy())
    return {
        'success': True,
        'last_update': Timeholder.get_time(),
        'data': items
    }
