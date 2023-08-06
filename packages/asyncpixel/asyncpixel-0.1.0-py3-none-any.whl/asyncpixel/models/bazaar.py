import datetime
from typing import List


class Bazaar_buy_summary:
    def __init__(self, amount: int, pricePerUnit: int, orders: int):
        self.amount = amount
        self.pricePerUnit = pricePerUnit
        self.orders = orders


class Bazaar_sell_summary:
    def __init__(self, amount: int, pricePerUnit: int, orders: int):
        self.amount = amount
        self.pricePerUnit = pricePerUnit
        self.orders = orders


class Bazaar_quick_status:
    def __init__(
        self,
        productId: str,
        sellPrice: float,
        sellVolume: int,
        sellMovingWeek: int,
        sellOrders: int,
        buyPrice: float,
        buyVolume: int,
        buyMovingWeek: int,
        buyOrders: int,
    ):
        self.productId = productId
        self.sellPrice = sellPrice
        self.sellVolume = sellVolume
        self.sellMovingWeek = sellMovingWeek
        self.sellOrders = sellOrders
        self.buyPrice = sellPrice
        self.buyVolume = sellVolume
        self.buyMovingWeek = sellMovingWeek
        self.buyOrders = sellOrders


class Bazaar:
    def __init__(self, lastUpdated: datetime.datetime, bazaar_items: List):
        self.lastUpdated = lastUpdated
        self.bazaar_items = bazaar_items


class Bazaar_item:
    def __init__(
        self,
        name: str,
        product_id: str,
        sell_summary: Bazaar_sell_summary,
        buy_summary: Bazaar_buy_summary,
        quick_status: List[Bazaar_quick_status],
    ):
        self.name = name
        self.product_id = product_id
        self.sell_summary = sell_summary
        self.buy_summary = buy_summary
        self.quick_status = quick_status
