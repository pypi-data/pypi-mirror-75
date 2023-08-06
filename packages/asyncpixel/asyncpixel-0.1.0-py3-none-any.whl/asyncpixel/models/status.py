class Status:
    def __init__(self, online: bool, gameType=None, _mode=None, _map=None):
        self.online = online
        self.gameType = gameType
        self.mode = _mode
        self.map = _map
