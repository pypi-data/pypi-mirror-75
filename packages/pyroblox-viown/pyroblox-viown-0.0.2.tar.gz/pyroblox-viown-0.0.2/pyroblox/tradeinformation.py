from .utils.errors import InvalidParameters
from .item import Item

class TradeInformation:
    def __init__(self, requests, tradeId=None):
        if not tradeId:
            raise InvalidParameters("Missing parameter: `tradeId`")
        self.requests = requests
        self.id = tradeId
        """Gets the id of the trade"""
        self.trade = requests.get(f"https://trades.roblox.com/v1/trades/{str(self.id)}").json()

    def offered(self):
        """
        Items that you've offered in the trade
        """
        items = []
        for offer in self.trade["offers"][0]["userAssets"]:
            items.append(Item(offer["name"], offer["id"], offer["assetId"], offer["recentAveragePrice"]))
        return items

    def requested(self):
        """
        Items that you've requested in the trade
        """
        items = []
        for offer in self.trade["offers"][1]["userAssets"]:
            items.append(Item(offer["name"], offer["id"], offer["assetId"], offer["recentAveragePrice"]))
        return items

    def robuxOffered(self):
        """
        Amount of robux that you've offered in the trade
        """
        return self.trade["offers"][0]["robux"]

    def robuxRequested(self):
        """
        Amount of robux that you've requested in the trade
        """
        return self.trade["offers"][1]["robux"]