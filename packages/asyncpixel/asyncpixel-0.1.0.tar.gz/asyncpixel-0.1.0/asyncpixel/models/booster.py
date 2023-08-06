import datetime
from typing import List


class Booster:
    def __init__(
        self,
        _id: str,
        purchaserUuid: str,
        amount: int,
        originalLength: int,
        length: int,
        gameType: int,
        dateActivated: datetime.datetime,
        stacked: bool = False,
    ):

        self._id = _id
        self.purchaserUuid = purchaserUuid
        self.amount = amount
        self.originalLength = originalLength
        self.length = length
        self.gameType = gameType
        self.dateActivated = dateActivated
        self.stacked = stacked


class Boosters:
    def __init__(
        self, boosterStatedecrementing: bool, boosters: List[Booster]
    ):
        self.boosterStatedecrementing = boosterStatedecrementing
        self.boosters = boosters
