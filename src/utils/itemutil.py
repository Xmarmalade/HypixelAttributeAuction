import nbt
from nbt.nbt import TAG_List, TAG_Compound
import io
import base64
import traceback

from fastapi.encoders import jsonable_encoder

from models.response import AuctionData, Attribute

class ItemUtil():
    @staticmethod
    def convertNBTToJson(raw_data: str) -> dict:
        try:
            nbtdata = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw_data)))['i'][0]
            data = jsonable_encoder(ItemUtil._unpack_nbt(nbtdata))
            return {'nbtdata': data}
        except Exception as e:
            print('data: ')
            print(raw_data)
            traceback.print_exc()

    @staticmethod
    def get_attributes_from_item_bytes(raw_data: str) -> tuple[list[Attribute], str]:
        attributes: list[Attribute] = []
        item_id = ''
        try:
            nbtdata = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw_data)))['i'][0]
            if 'attributes' in nbtdata['tag']['ExtraAttributes']:
                attribute_keys = nbtdata['tag']['ExtraAttributes']['attributes'].keys()
                for key in attribute_keys:
                    data: Attribute = {
                        'name': key,
                        'value': int(nbtdata['tag']['ExtraAttributes']['attributes'][key].valuestr())
                    }
                    attributes.append(data.copy())
            if 'id' in nbtdata['tag']['ExtraAttributes']:
                item_id = nbtdata['tag']['ExtraAttributes']['id'].valuestr()
            return attributes, item_id
        except Exception as e:
            print('data: ')
            print(raw_data)
            traceback.print_exc()

    @staticmethod
    def organize_item_data(raw_item_data: dict, all = False) -> AuctionData:
        try:
            item_data = raw_item_data
            attributes = {}
            item_id = ''
            if all:
                attributes, item_id = ItemUtil.get_attributes_from_item_bytes(item_data['item_bytes'])
            else:
                attributes, item_id = ItemUtil.get_attributes_from_item_bytes(item_data['item_bytes']['data'])
            # re-organize data
            isBin = False
            if 'bin' in item_data and item_data['bin'] == True:
                isBin = True
            data: AuctionData = {
                'uuid': item_data['uuid'],
                'auctioneer': item_data['auctioneer'],
                'profile_id': item_data['profile_id'],
                'start_unix': item_data['start'],
                'end_unix': item_data['end'],
                'item_name': item_data['item_name'],
                'item_id': item_id,
                'item_lore_raw': item_data['item_lore'],
                'rarity': item_data['tier'],
                'price': item_data['starting_bid'],
                'attributes': attributes,
                'claimed': item_data['claimed'],
                'bin': isBin,
                'highest_bid': item_data['highest_bid_amount']
                #'bids': item_data['bids']
            }
            return data
        except Exception as e:
            print('data: ')
            print(raw_item_data)
            traceback.print_exc()

    @staticmethod
    def _unpack_nbt(tag):
        """
        Unpack an NBT tag into a native Python data structure.
        Taken from https://github.com/twoolie/NBT/blob/master/examples/utilities.py
        """
        if isinstance(tag, TAG_List):
            return [ItemUtil._unpack_nbt(i) for i in tag.tags]
        elif isinstance(tag, TAG_Compound):
            return dict((str(i.name), ItemUtil._unpack_nbt(i)) for i in tag.tags)
        else:
            return tag.value
        
    @staticmethod
    def check_attribute(auction_data, attribute1: str = '', attribute2: str = '', attrlevel1: str = '', attrlevel2: str = ''):
        attribute_flag1: bool = None
        attribute_flag2: bool = None
        if attrlevel1 == '': attrlevel1 = '1'
        if attrlevel2 == '': attrlevel2 = '1'
        if attribute1 != '': attribute_flag1 = False
        if attribute2 != '': attribute_flag2 = False
        for attribute in auction_data['attributes']:
            if (attribute1 != '' and attribute['name'] == attribute1) and (attribute['value'] >= int(attrlevel1)):
                attribute_flag1 = True
            if (attribute2 != '' and attribute['name'] == attribute2) and (attribute['value'] >= int(attrlevel2)):
                attribute_flag2 = True
        if attribute_flag1 == False or attribute_flag2 == False:
            return False
        else:
            return True
