import datetime


class Game:
    def __init__(
        self,
        date: datetime.datetime,
        gameType: str,
        mode: str,
        _map: str,
        ended: datetime.datetime = None,
    ):
        self.date = date
        self.gameType = gameType
        self.mode = mode
        self.map = _map
        self.ended = ended
