import datetime


class Friend:
    def __init__(
        self,
        _id: str,
        uuidSender: str,
        uuidReceiver: str,
        started: datetime.datetime,
    ):
        self._id = _id
        self.uuidSender = uuidSender
        self.uuidReceiver = uuidReceiver
        self.started = started
