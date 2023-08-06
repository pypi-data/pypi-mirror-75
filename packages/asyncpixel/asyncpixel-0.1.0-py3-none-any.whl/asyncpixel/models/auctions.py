import datetime
from typing import List


class Auction:
    def __init__(
        self,
        page: str,
        totalPages: str,
        totalAuctions: str,
        lastUpdated: datetime.datetime,
        auctions: str,
    ):
        self.page = page
        self.totalPages = totalPages
        self.totalAuctions = totalAuctions
        self.lastUpdated = lastUpdated
        self.auctions = auctions


class Auction_item:
    def __init__(
        self,
        uuid: str,
        auctioneer: str,
        profile_id: str,
        coop: List[str],
        start: datetime.datetime,
        end: datetime.datetime,
        item_name: str,
        item_lore: str,
        extra: str,
        category: str,
        tier: str,
        starting_bid: int,
        item_bytes: str,
        claimed: bool,
        claimed_bidders: List,
        highest_bid_amount: int,
        bids: List,
        _id: str = None,
    ):
        self.id = _id
        self.uuid = uuid
        self.auctioneer = auctioneer
        self.profile_id = profile_id
        self.coop = coop
        self.start = start
        self.end = end
        self.item_name = item_name
        self.item_lore = item_lore
        self.extra = extra
        self.category = category
        self.tier = tier
        self.starting_bid = starting_bid
        self.item_bytes = item_bytes
        self.claimed = claimed
        self.claimed_bidders = claimed_bidders
        self.highest_bid_amount = highest_bid_amount
        self.bids = bids

