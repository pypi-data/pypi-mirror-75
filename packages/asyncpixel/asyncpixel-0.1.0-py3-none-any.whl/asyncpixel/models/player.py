import datetime
from typing import List


class Player:
    def __init__(
        self,
        _id: str,
        uuid: str,
        firstLogin: datetime.datetime,
        playername: str,
        lastLogin: datetime.datetime,
        displayname: str,
        knownAliases: List[str],
        knownAliasesLower: List[str],
        achievementsOneTime: List[str],
        mcVersionRp: str,
        networkExp: int,
        karma: int,
        spec_always_flying: bool,
        lastAdsenseGenerateTime: datetime.datetime,
        lastClaimedReward: int,
        totalRewards: int,
        totalDailyRewards: int,
        rewardStreak: int,
        rewardScore: int,
        rewardHighScore: int,
        lastLogout: datetime.datetime,
        friendRequestsUuid: List[str],
        network_update_book: str,
        achievementTracking: List[str],
        achievementPoints: int,
        currentGadget: str,
        channel: str,
        mostRecentGameType: str,
        level: int,
    ):
        self.id = _id
        self.uuid = uuid
        self.firstLogin = firstLogin
        self.playername = playername
        self.lastLogin = lastLogin
        self.displayname = displayname
        self.knownAliases = knownAliases
        self.knownAliasesLower = knownAliasesLower
        self.achievementsOneTime = achievementsOneTime
        self.mcVersionRp = mcVersionRp
        self.networkExp = networkExp
        self.karma = karma
        self.spec_always_flying = spec_always_flying
        self.lastAdsenseGenerateTime = lastAdsenseGenerateTime
        self.lastClaimedReward = lastClaimedReward
        self.totalRewards = totalRewards
        self.totalDailyRewards = totalDailyRewards
        self.rewardStreak = rewardStreak
        self.rewardScore = rewardScore
        self.rewardHighScore = rewardHighScore
        self.lastLogout = lastLogout
        self.friendRequestsUuid = friendRequestsUuid
        self.network_update_book = network_update_book
        self.achievementTracking = achievementTracking
        self.achievementsPoints = achievementPoints
        self.currentGadget = currentGadget
        self.channel = channel
        self.mostRecentGameType = mostRecentGameType
        self.level = level

