from .utils.errors import HTTPError, InvalidFilterType, InvalidTrade
from .item import Item
from .data.AssetTypes import assettypes
from .trade import Trade
import json

class User:
    def __init__(self, requests, userid=None):
        """
        Represents a user
        """
        self.id = userid
        """ID of the user"""
        self.requests = requests
        self.filters = assettypes

    def name(self):
        """Name of the user"""
        return self.requests.get(f"https://api.roblox.com/users/{str(self.id)}").json()["Username"]

    def status(self):
        """
        Gets the users status
        """
        r = self.requests.get(f"https://users.roblox.com/v1/users/{str(self.id)}/status")
        if r.status_code == 200:
            return r.json()["status"]
        else:
            raise HTTPError(
                f"HTTP error occured with status code {str(r.status_code)}")

    def follow(self):
        """
        Follows the user
        """
        r = self.requests.post(f"https://friends.roblox.com/v1/users/{str(self.id)}/follow")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def unfollow(self):
        """
        Unfollows the user
        """
        r = self.requests.post(f"https://friends.roblox.com/v1/users/{str(self.id)}/unfollow")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def block(self):
        """
        Blocks the user
        """
        data = {
            "blockeeId": self.id
        }
        r = self.requests.post("https://www.roblox.com/userblock/blockuser", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def unblock(self):
        """
        Unblocks the user
        """
        data = {
            "blockeeId": self.id
        }
        r = self.requests.post("https://www.roblox.com/userblock/unblockuser", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")


    def add(self):
        """
        Sends a friend request to the user.
        """
        r = self.requests.post(f"https://friends.roblox.com/v1/users/{str(self.id)}/request-friendship")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def message(self, subject : str, body : str):
        """
        Messages the user
        """
        data = {
            "subject": subject,
            "body": body,
            "recipientid": self.id
        }
        r = self.requests.post("https://privatemessages.roblox.com/v1/messages/send", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def send_trade(self, offer : list, request : list, offerRobux=0, requestRobux=0):
        """
        Sends a trade to the user.
        This function takes user asset ids instead of assetids,
        to get the users inventory call user.inventory(filter="Collectibles") and it will get all limited items that the user owns
        along with the user asset ids.
        """
        if len(offer) > 4 or len(request) > 4:
            raise InvalidTrade("Too many items requested, limit is `4`")
        account = self.requests.get("https://users.roblox.com/v1/users/authenticated").json()["id"]
        data = {
            "offers": [
                {
                    "userId": self.id,
                    "userAssetIds": request,
                    "robux": offerRobux
                },
                {
                    "userId": account,
                    "userAssetIds": offer,
                    "robux": requestRobux
                }
            ]
        }
        r = self.requests.post("https://trades.roblox.com/v1/trades/send", data=json.dumps(data))
        if r.status_code == 200:
            return Trade(self.requests, r.json()["id"])
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def inventory(self, filter="Default"):
        """
        Returns the users inventory. By default this will return the list of hats a user owns.
        To view a list of asset types, go to: https://developer.roblox.com/en-us/api-reference/enum/AssetType
        """
        if filter.lower() in ["collectibles", "limiteds"]:
            r = self.requests.get(f"https://inventory.roblox.com/v1/users/{str(self.id)}/assets/collectibles?limit=100")
            if r.status_code == 200:
                data = r.json()["data"]
                d = []
                for item in data:
                    d.append(Item(item["name"], item["userAssetId"], item["assetId"], item["recentAveragePrice"]))
                return d
            else:
                return HTTPError(f"HTTP error occured with status code {str(r.status_code)}")
        else:
            if filter in self.filters:
                r = self.requests.get(f"https://inventory.roblox.com/v2/users/{str(self.id)}/inventory/{self.filters[filter]}")
                data = r.json()["data"]
                d = []
                for item in data:
                    d.append(Item(item["assetName"], item["userAssetId"], item["assetId"], False, item["owner"]["userId"], item["owner"]["username"], item["created"], item["updated"]))
                return d
            else:
                raise InvalidFilterType(f"Unknown filter type {filter}, check the documentation for a list of filter types.")

    def games(self):
        """
        Returns a list of games the user has created
        """
        pass