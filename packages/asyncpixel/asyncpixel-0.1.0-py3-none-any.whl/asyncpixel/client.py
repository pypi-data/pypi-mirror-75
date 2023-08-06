"""
A Python HypixelAPI wrapper.
"""

import datetime as dt
from typing import Dict, List

import aiohttp

from .exceptions.exceptions import ApiNoSuccess, RateLimitError
from .models.auctions import Auction, Auction_item
from .models.bazaar import (
    Bazaar,
    Bazaar_buy_summary,
    Bazaar_item,
    Bazaar_quick_status,
    Bazaar_sell_summary,
)
from .models.booster import Booster, Boosters
from .models.friends import Friend
from .models.guild import Guild

from .models.games import Game
from .models.key import Key
from .models.news import News

from .models.player import Player
from .models.status import Status
from .models.watchdog import WatchDog

BASE_URL = "https://api.hypixel.net/"


class Client:
    """client class for hypixel wrapper."""

    def __init__(self, api_key: str):
        """Initialise base class by storing keys and creating session

        Args:
            api_key (str): hypixel api key
        """

        # Handles the instance of a singular key

        self.api_key = api_key

        self.session = aiohttp.ClientSession()

    async def close(self):
        """used for safe client cleanup and stuff."""
        await self.session.close()

    async def get(self, path: str, params: Dict = {}) -> dict:
        """Base function to get raw data from hypixel

        Args:
            path (str): path that you wish to request from
            params (Dict, optional): parameters to pass into request.
            Defaults to empty dictionary.

        Raises:
            RateLimitError: error if ratelimit has been reached

        Returns:
            dict: returns a dictionary of the json response
        """
        params["key"] = self.api_key

        response = await self.session.get(f"{BASE_URL}{path}", params=params)

        if response.status == 429:
            raise RateLimitError("Hypixel")

        response = await response.json()

        if not response["success"]:
            raise ApiNoSuccess()

        return response

    async def get_watchdog_stats(self) -> WatchDog:
        """Get current watchdog stats.

        Returns:
            WatchDog: WatchDog stats object
        """
        data = await self.get("watchdogstats")

        return WatchDog(
            watchdog_lastMinute=data["watchdog_lastMinute"],
            staff_rollingDaily=data["staff_rollingDaily"],
            watchdog_total=data["watchdog_total"],
            watchdog_rollingDaily=data["watchdog_rollingDaily"],
            staff_total=data["staff_total"],
        )

    async def get_key_data(self, key: str = None) -> Key:
        """Get information about an api key.

        Args:
            key (str, optional): api key. Defaults tokey provided in class.

        Returns:
            Key: Key object
        """

        if key is None:
            key = self.api_key

        data = await self.get("key")

        return Key(
            key=data["record"]["key"],
            owner=data["record"]["owner"],
            limit=data["record"]["limit"],
            queriesInPastMin=data["record"]["queriesInPastMin"],
            totalQueries=data["record"]["totalQueries"],
        )

    async def get_boosters(self) -> Boosters:
        """Get the current online boosters.

        Returns:
            Boosters: object containing boosters
        """
        data = await self.get("boosters")
        boosterlist = []

        for boost in data["boosters"]:
            boosterlist.append(
                Booster(
                    _id=boost["_id"],
                    purchaserUuid=boost["purchaserUuid"],
                    amount=boost["amount"],
                    originalLength=boost["originalLength"],
                    length=boost["length"],
                    gameType=boost["gameType"],
                    dateActivated=dt.datetime.fromtimestamp(
                        boost["dateActivated"] / 1000
                    ),
                    stacked=boost["stacked"] if "stacked" in boost else False,
                )
            )
        return Boosters(
            boosterStatedecrementing=data["boosterState"]["decrementing"],
            boosters=boosterlist,
        )

    async def get_player_count(self) -> int:
        """Get the current amount of players online.

        Returns:
            int: number of online players
        """
        data = await self.get("playerCount")

        return data["playerCount"]

    async def get_news(self) -> List[News]:
        """Get current skyblock news.

        Returns:
            List[News]: List of news objects
        """
        data = await self.get("skyblock/news")
        news_list = []
        for item in data["items"]:
            news_list.append(
                News(
                    material=item["item"]["material"],
                    link=item["link"],
                    text=item["text"],
                    title=item["title"],
                )
            )

        return news_list

    async def get_player_status(self, uuid: str) -> Status:
        """Get current online status about a player.

        Args:
            uuid (str): uuid of player

        Returns:
            Status: Status object of player
        """

        data = await self.get("status", params={"uuid": uuid})
        if data["session"]["online"]:
            return Status(
                online=True,
                gameType=data["session"]["gameType"],
                mode=data["session"]["mode"],
                map=data["session"],
            )
        return Status(online=False)

    async def get_player_friends(self, uuid: str) -> List[Friend]:
        """Get a list of a players friends

        Args:
            uuid (str): the uuid of the player you wish to get friends from

        Returns:
            List[Friend]: returns a list of friend elements
        """

        params = {"uuid": uuid}
        data = await self.get("friends", params=params)

        if not data["success"]:
            return None

        friend_list = []
        for friend in data["records"]:
            friend_list.append(
                Friend(
                    _id=friend["_id"],
                    uuidSender=friend["uuidSender"],
                    uuidReceiver=friend["uuidReceiver"],
                    started=dt.datetime.fromtimestamp(
                        friend["started"] / 1000
                    ),
                )
            )

        return friend_list

    async def get_bazaar(self) -> Bazaar:
        """Get info of the items in the bazaar.

        Returns:
            Bazaar: object for bazzar
        """

        data = await self.get("skyblock/bazaar")

        bazaar_items = []

        for name in data["products"]:
            elements = data["products"][name]
            sell_summary = []
            buy_summary = []
            for sell in elements["sell_summary"]:
                sell_summary.append(
                    Bazaar_sell_summary(
                        amount=sell["amount"],
                        pricePerUnit=sell["pricePerUnit"],
                        orders=sell["orders"],
                    )
                )
            for buy in elements["buy_summary"]:
                buy_summary.append(
                    Bazaar_buy_summary(
                        amount=buy["amount"],
                        pricePerUnit=buy["pricePerUnit"],
                        orders=buy["orders"],
                    )
                )
            quick = elements["quick_status"]
            bazaar_quick_status = Bazaar_quick_status(
                productId=quick["productId"],
                sellPrice=quick["sellPrice"],
                sellVolume=quick["sellVolume"],
                sellMovingWeek=quick["sellMovingWeek"],
                sellOrders=quick["sellOrders"],
                buyPrice=quick["buyPrice"],
                buyVolume=quick["buyVolume"],
                buyMovingWeek=quick["buyMovingWeek"],
                buyOrders=quick["buyOrders"],
            )
            bazaar_items.append(
                Bazaar_item(
                    name=name,
                    product_id=elements["product_id"],
                    sell_summary=sell_summary,
                    buy_summary=buy_summary,
                    quick_status=bazaar_quick_status,
                )
            )

        return Bazaar(
            lastUpdated=dt.datetime.fromtimestamp(1590854517479 / 1000),
            bazaar_items=bazaar_items,
        )

    async def auctions(self, page: int = 0) -> Auction:
        """Get the auctions available.

        Args:
            page (int, optional): Page of auction list you want. Defaults to 0.

        Returns:
            Auction: Auction object.
        """

        params = {"page": page}
        data = await self.get("skyblock/auctions", params=params)
        auction_list = []
        for auc in data["auctions"]:
            auction_list.append(
                Auction_item(
                    uuid=auc["uuid"],
                    auctioneer=auc["auctioneer"],
                    profile_id=auc["profile_id"],
                    coop=auc["coop"],
                    start=dt.datetime.fromtimestamp(auc["start"] / 1000),
                    end=dt.datetime.fromtimestamp(auc["end"] / 1000),
                    item_name=auc["item_name"],
                    item_lore=auc["item_lore"],
                    extra=auc["extra"],
                    category=auc["category"],
                    tier=auc["tier"],
                    starting_bid=auc["starting_bid"],
                    item_bytes=auc["item_bytes"],
                    claimed=auc["claimed"],
                    claimed_bidders=auc["claimed_bidders"],
                    highest_bid_amount=auc["highest_bid_amount"],
                    bids=auc["bids"],
                )
            )
        return Auction(
            page=data["page"],
            totalPages=data["totalPages"],
            totalAuctions=data["totalAuctions"],
            lastUpdated=dt.datetime.fromtimestamp(data["lastUpdated"] / 1000),
            auctions=auction_list,
        )

    async def get_recent_games(self, uuid: str) -> List[Game]:
        """Get recent games of a player

        Args:
            uuid (str): uuid of player

        Returns:
            List[Game]: list of recent games
        """

        params = {"uuid": uuid}
        data = await self.get("recentGames", params=params)

        if not data["success"]:
            return None

        games_list = []
        for game in data["games"]:
            if "ended" in game:
                games_list.append(
                    Game(
                        date=dt.datetime.fromtimestamp(game["date"] / 1000),
                        gameType=game["gameType"],
                        mode=game["Mode"],
                        _map=game["map"],
                        ended=dt.datetime.fromtimestamp(game["ended"] / 1000),
                    )
                )
            else:
                games_list.append(
                    Game(
                        data=dt.datetime.fromtimestamp(game["date"] / 1000),
                        gameType=game["gameType"],
                        mode=game["Mode"],
                        _map=game["map"],
                    )
                )

        return games_list

    async def get_player(self, uuid: str) -> Player:
        """Get information about a player from their uuid

        Args:
            uuid (str): uuid of player

        Returns:
            Player: player object
        """
        params = {"uuid": uuid}
        data = await self.get("player", params=params)

        return Player(
            _id=data["player"]["_id"],
            uuid=data["player"]["uuid"],
            firstLogin=dt.datetime.fromtimestamp(
                data["player"]["firstLogin"] / 1000
            ),
            playername=data["player"]["playername"],
            lastLogin=dt.datetime.fromtimestamp(
                data["player"]["lastLogin"] / 1000
            ),
            displayname=data["player"]["displayname"],
            knownAliases=data["player"]["knownAliases"],
            knownAliasesLower=data["player"]["knownAliasesLower"],
            achievementsOneTime=data["player"]["achievementsOneTime"],
            mcVersionRp=data["player"]["mcVersionRp"],
            networkExp=data["player"]["networkExp"],
            karma=data["player"]["karma"],
            spec_always_flying=data["player"]["spec_always_flying"],
            lastAdsenseGenerateTime=data["player"]["lastAdsenseGenerateTime"],
            lastClaimedReward=data["player"]["lastClaimedReward"],
            totalRewards=data["player"]["totalRewards"],
            totalDailyRewards=data["player"]["totalDailyRewards"],
            rewardStreak=data["player"]["rewardStreak"],
            rewardScore=data["player"]["rewardScore"],
            rewardHighScore=data["player"]["rewardHighScore"],
            lastLogout=dt.datetime.fromtimestamp(
                data["player"]["lastLogout"] / 1000
            ),
            friendRequestsUuid=data["player"]["friendRequestsUuid"],
            network_update_book=data["player"]["network_update_book"],
            achievementTracking=data["player"]["achievementTracking"],
            achievementPoints=data["player"]["achievementPoints"],
            currentGadget=data["player"]["currentGadget"],
            channel=data["player"]["channel"],
            mostRecentGameType=data["player"]["mostRecentGameType"],
            level=self.calcPlayerLevel(data["player"]["networkExp"]),
        )

    @staticmethod
    def calcPlayerLevel(xp: int) -> int:
        """Calculate player level from xp.

        Args:
            xp (int): amount of xp a player has

        Returns:
            int: currentl level of player
        """
        return int(1 + (-8750.0 + (8750 ** 2 + 5000 * xp) ** 0.5) / 2500)

    async def find_guild_by_name(self, name: str) -> str:
        """Find guild id by name.

        Args:
            name (str): name of guild

        Returns:
            str: id of guild
        """
        params = {"byName": name}
        data = await self.get("findGuild", params=params)
        return data["guild"]

    async def find_guild_by_uuid(self, uuid: str) -> str:
        """Find guild by uuid

        Args:
            uuid (str): uuid of guild

        Returns:
            str: id of guild
        """
        params = {"byUuid": uuid}
        data = await self.get("findGuild", params=params)
        return data["guild"]

    async def get_guild_by_name(self, guild_name: str) -> Guild:
        """Get guild by name

        Args:
            guild_name (str): name of guild

        Returns:
            Guild: guild object
        """

        params = {"name": guild_name}
        data = await self.get("guild", params=params)
        guild_object = await self.create_guild_object(data)
        return guild_object

    async def get_guild_by_id(self, guild_id: int) -> Guild:
        """Get guild by id

        Args:
            guild_id (str): id of guild

        Returns:
            Guild: guild object
        """
        params = {"id": guild_id}
        data = await self.get("guild", params=params)
        guild_object = await self.create_guild_object(data)
        return guild_object

    async def get_guild_by_player(self, player_uuid: str) -> Guild:
        """Get guild by player

        Args:
            player_uuid (str): uuid of a player in the guild

        Returns:
            Guild: guild object
        """
        params = {"player": player_uuid}
        data = await self.get("guild", params=params)
        guild_object = await self.create_guild_object(data)
        return guild_object

    @staticmethod
    def create_guild_object(data) -> Guild:
        guild = data["guild"]
        return Guild(
            _id=guild["_id"],
            created=dt.datetime.fromtimestamp(guild["created"] / 1000),
            name=guild["name"],
            name_lower=guild["name_lower"],
            description=guild["description"],
            tag=guild["tag"],
            tagColor=guild["tagColor"],
            exp=guild["exp"],
            members=guild["members"],
            achievements=guild["achievements"],
            ranks=guild["ranks"],
            joinable=guild["joinable"],
            legacyRanking=guild["legacyRanking"],
            publiclyListed=guild["publiclyListed"],
            hideGmTag=guild["hideGmTag"],
            preferredGames=guild["preferredGames"],
            chatMute=guild["chatMute"],
            guildExpByGameType=guild["guildExpByGameType"],
            banner=guild["banner"],
        )

    async def get_profile(self, profile: str) -> Dict:
        """Get profile info of a skyblock player.

        Args:
            _profile (str): profile id of player ca be gotten from
                            running get_profiles

        Returns:
            Dict: json reponse
        """

        params = {"profile": profile}
        data = await self.get("skyblock/profile", params=params)
        return data["profile"]

    async def get_profiles(self, uuid: str) -> Dict:
        """Get info on a profile.

        Args:
            uuid (str): uuid of player

        Returns:
            Dict: json response
        """

        params = {"uuid": uuid}
        data = await self.get("skyblock/profiles", params=params)
        return data["profiles"]

    async def get_auction_from_uuid(self, uuid: str) -> List[Auction_item]:
        params = {"uuid": uuid}
        data = await self.get("skyblock/auction", params=params)
        auction_items = self.create_auction_object(data)
        return auction_items

    async def get_auction_from_player(self, player: str) -> List[Auction_item]:
        params = {"player": player}
        data = await self.get("skyblock/auction", params=params)
        auction_items = self.create_auction_object(data)
        return auction_items

    async def get_auction_from_profile(
        self, profile_id: str
    ) -> List[Auction_item]:
        params = {"profile": profile_id}
        data = await self.get("skyblock/auction", params=params)
        auction_items = self.create_auction_object(data)
        return auction_items

    @staticmethod
    def create_auction_object(data) -> List[Auction_item]:
        auction_list = []
        for auc in data["auctions"]:
            auction_list.append(
                Auction_item(
                    _id=auc["_id"],
                    uuid=auc["uuid"],
                    auctioneer=auc["auctioneer"],
                    profile_id=auc["profile_id"],
                    coop=auc["coop"],
                    start=dt.datetime.fromtimestamp(auc["start"] / 1000),
                    end=dt.datetime.fromtimestamp(auc["end"] / 1000),
                    item_name=auc["item_name"],
                    item_lore=auc["item_lore"],
                    extra=auc["extra"],
                    category=auc["category"],
                    tier=auc["tier"],
                    starting_bid=auc["starting_bid"],
                    item_bytes=auc["item_bytes"],
                    claimed=auc["claimed"],
                    claimed_bidders=auc["claimed_bidders"],
                    highest_bid_amount=auc["highest_bid_amount"],
                    bids=auc["bids"],
                )
            )
        return auction_list

    # NOT FULLY IMPLEMENTED

    async def get_game_count(self) -> dict:
        """Get the current game count

        Returns:
            dict: raw json response
        """

        data = await self.get("gameCounts")
        return data["games"]

    async def get_leaderboard(self) -> dict:
        """Get the current leaderboards

        Returns:
            dict: raw json response
        """

        data = await self.get("leaderboards")
        return data["leaderboards"]

    async def get_resources_achievements(self) -> dict:
        """Get the current resources. Does not require api key

        Returns:
            dict: raw json response
        """
        data = await self.get("resources/achievements")
        return data["achievements"]

    async def get_resources_challenges(self) -> dict:
        """Get the current resources. Does not require api key

        Returns:
            dict: raw json response
        """
        data = await self.get("resources/challenges")
        return data["challenges"]

    async def get_resources_quests(self) -> dict:
        """Get the current resources. Does not require api key

        Returns:
            dict: raw json response
        """
        data = await self.get("resources/quests")
        return data["quests"]

    async def get_resources_guilds_achievements(self) -> dict:
        """Get the current resources. Does not require api key

        Returns:
            dict: raw json response
        """
        data = await self.get("resources/guilds/achievements")
        return data["guilds/achievements"]

    async def get_resources_guilds_permissions(self) -> dict:
        """Get the current resources. Does not require api key

        Returns:
            dict: raw json response
        """
        data = await self.get("resources/guilds/permissions")
        return data["guilds/permissions"]

    async def get_resources_skyblock_collections(self) -> dict:
        """Get the current resources. Does not require api key

        Returns:
            dict: raw json response
        """
        data = await self.get("resources/skyblock/collections")
        return data["skyblock/collections"]

    async def get_resources_skyblock_skills(self) -> dict:
        """Get the current resources. Does not require api key

        Returns:
            dict: raw json response
        """
        data = await self.get("resources/skyblock/skills")
        return data["skyblock/skills"]
