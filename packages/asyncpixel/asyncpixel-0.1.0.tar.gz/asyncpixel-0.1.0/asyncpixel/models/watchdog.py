class WatchDog:
    def __init__(
        self,
        watchdog_lastMinute,
        staff_rollingDaily,
        watchdog_total,
        watchdog_rollingDaily,
        staff_total,
    ):
        """Base class for watchdog stat."""
        self.watchdog_lastMinute = watchdog_lastMinute
        self.staff_rollingDaily = staff_rollingDaily
        self.watchdog_total = watchdog_total
        self.watchdog_rollingDaily = watchdog_rollingDaily
        self.staff_total = staff_total
