import aiohttp
import os
import time
import sys
import traceback
from typing import Union

from utils.itemutil import ItemUtil
from utils.statushandle import handle_status_code
from models.response import AuctionResponse, MultipleAuctionResponse, EmptyResponse, AuctionData
from utils.timeholder import Timeholder

class HypixelAPI():
    def __init__(self) -> None:
        self.session = aiohttp.ClientSession('https://api.hypixel.net')
        self._api_key = os.environ['HYPIXEL_API_KEY']
        self._base_params = {'key': self._api_key}

    async def get_auction_by_auction_id(self, auction_id: str) -> AuctionResponse:
        async with self.session.get(url='/skyblock/auction', params={**self._base_params, **{'uuid': auction_id}}) as r:
            status_code = r.status
            handle_status_code(status_code=status_code)
            try:
                json = await r.json()
                if json['auctions'] == []:
                    data: AuctionResponse = {
                        'success': True,
                        'data': None
                    }
                    return data
                item_data = json['auctions'][0]
                organized_item_data = ItemUtil.organize_item_data(item_data)
                last_update = Timeholder.get_time()
                data: AuctionResponse = {
                    'success': True,
                    'last_update': last_update,
                    'data': organized_item_data
                }
                return data
            except Exception as e:
                print('data: ')
                print(json)
                traceback.print_exc()

    async def get_active_auction_by_uuid(self, uuid: str) -> Union[MultipleAuctionResponse, EmptyResponse]:
        async with self.session.get(url='/skyblock/auction', params={**self._base_params, **{'player': uuid}}) as r:
            status_code = r.status
            handle_status_code(status_code=status_code)
            try:
                json = await r.json()
                auction_list = []
                current_unix = int(time.time()*1000)
                for i in json['auctions']:
                    if i['end'] < current_unix:
                        continue
                    item_data = ItemUtil.organize_item_data(i)
                    auction_list.append(item_data.copy())
                last_update = Timeholder.get_time()
                if auction_list == []:
                    data: EmptyResponse = {
                        'success': True,
                        'last_update': last_update,
                        'data': []
                    }
                else:
                    data: MultipleAuctionResponse = {
                        'success': True,
                        'last_update': last_update,
                        'data': auction_list
                    }
                return data
            except Exception as e:
                print('data: ')
                print(json)
                traceback.print_exc()

    async def get_active_auction_by_profileid(self, profile_id: str) -> Union[MultipleAuctionResponse, EmptyResponse]:
        async with self.session.get(url='/skyblock/auction', params={**self._base_params, **{'profile': profile_id}}) as r:
            status_code = r.status
            handle_status_code(status_code=status_code)
            try:
                json = await r.json()
                auction_list = []
                current_unix = int(time.time()*1000)
                for i in json['auctions']:
                    if i['end'] < current_unix:
                        continue
                    item_data = ItemUtil.organize_item_data(i)
                    auction_list.append(item_data.copy())
                last_update = Timeholder.get_time()
                if auction_list == []:
                    data: EmptyResponse = {
                        'success': True,
                        'last_update': last_update,
                        'data': []
                    }
                else:
                    data: MultipleAuctionResponse = {
                        'success': True,
                        'last_update': last_update,
                        'data': auction_list
                    }
                return data
            except Exception as e:
                print('data: ')
                print(json)
                traceback.print_exc()
        
    async def get_all_auctions(self) -> list[AuctionData]:
        total_page = 0
        auctions = []
        total_size = 0
        async with self.session.get(url='/skyblock/auctions', params={**self._base_params, **{'page': 0}}) as r:
            data = await r.json()
            total_page = data['totalPages']
            for i in data['auctions']:
                item_data = ItemUtil.organize_item_data(i, True)
                auctions.append(dict(item_data).copy())
                total_size += sys.getsizeof(item_data)
        for page_num in range(total_page):
            print('page: ', page_num)
            if page_num == 0:
                continue
            async with self.session.get(url='/skyblock/auctions', params={**self._base_params, **{'page': page_num}}) as r:
                data = await r.json()
                for i in data['auctions']:
                    item_data = ItemUtil.organize_item_data(i, True)
                    auctions.append(dict(item_data).copy())
                    total_size += sys.getsizeof(item_data)
        return auctions