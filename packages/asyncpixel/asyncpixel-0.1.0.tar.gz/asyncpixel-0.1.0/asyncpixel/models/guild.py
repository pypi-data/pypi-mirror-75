import datetime
from typing import List


class Guild:
    def __init__(
        self,
        _id: str,
        created: datetime.datetime,
        name: str,
        name_lower: str,
        description: str,
        tag: str,
        tagColor: str,
        exp: int,
        members: List,
        achievements,
        ranks,
        joinable: bool,
        legacyRanking: int,
        publiclyListed: bool,
        hideGmTag: bool,
        preferredGames: List[str],
        chatMute: datetime.datetime,
        guildExpByGameType,
        banner,
    ):
        self._id = _id
        self.created = created
        self.name = name
        self.name_lower = name_lower
        self.description = description
        self.tag = tag
        self.tagColour = tagColor
        self.exp = exp
        self.members = members
        self.achievements = achievements
        self.ranks = ranks
        self.joinable = joinable
        self.legacyRanking = legacyRanking
        self.publiclyListed = publiclyListed
        self.hideGmTag = hideGmTag
        self.prefferedGames = preferredGames
        self.chatMute = chatMute
        self.guildExpByGameTYpe = guildExpByGameType
        self.banner = banner
