class RateLimitError(Exception):
    """Raised when a ratelimit is reached"""

    def __init__(self, source="unknown source"):
        self.message = f"The {source}API ratelimit was reached!"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ApiNoSuccess(Exception):
    """Raised when a ratelimit is reached"""

    def __init__(self):
        self.message = "The method encountered an error on the hypixel side."
        super().__init__(self.message)

    def __str__(self):
        return self.message
