class Key:
    def __init__(self, key, owner, limit, queriesInPastMin, totalQueries):
        """Base class for watchdog stat"""
        self.key = key
        self.owner = owner
        self.limit = limit
        self.queriesInPastMin = queriesInPastMin
        self.totalQueries = totalQueries

