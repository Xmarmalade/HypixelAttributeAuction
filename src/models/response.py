from pydantic import BaseModel, Field
from typing import Optional

class Attribute(BaseModel):
    name: str
    value: int

class Bid(BaseModel):
    auction_id: str
    bidder: str
    profile_id: str
    amount: int
    timestamp: int

class AuctionData(BaseModel):
    uuid: str
    auctioneer: str
    profile_id: str
    start_unix: int
    end_unix: int
    item_name: str
    item_id: str
    item_lore_raw: str
    rarity: str
    price: int
    attributes: list[Attribute] = None    # make it pydantic compatible
    claimed: bool
    bin: bool
    highest_bid: int
    bids: list[Bid] = None  # make it pydantic compatible

class AuctionResponse(BaseModel):
    success: bool
    data: Optional[AuctionData] = Field(...)

class MultipleAuctionResponse(BaseModel):
    success: bool
    data: list[AuctionData] = None

class EmptyResponse(BaseModel):
    success: bool
    data: list[None] = []