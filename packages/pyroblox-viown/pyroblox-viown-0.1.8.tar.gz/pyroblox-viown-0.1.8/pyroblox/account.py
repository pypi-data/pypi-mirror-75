from .utils.errors import HTTPError, InvalidParameters, InternalError
from .user import User
from .friendrequest import FriendRequest
from .message import Message
from .game import Game
from .trade import Trade
from .gamepass import Gamepass
from .group.group import Group
import json

class Account:
    def __init__(self, requests, userId):
        """
        Represents the authenticated users account.
        This can be used to modify/get information about the user (i.e changing status, about, etc)
        This class can be accessed through login.account
        """
        self.requests = requests
        self.id = userId
        """UserID of the account"""

    def update_status(self, status=None):
        """
        Updates your accounts status
        """
        if status:
            data = {
                "status": status
            }
            r = self.requests.post("https://www.roblox.com/home/updatestatus", data=json.dumps(data))
            if r.status_code == 200:
                return True
            else:
                raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def get_user(self, id=None, username=None):
        """
        Returns a User object, you can get the user either by id or username.
        """
        user = None
        if id:
            user = self.requests.get(f"https://api.roblox.com/users/{id}")
        elif username:
            user = self.requests.get(
                f"https://api.roblox.com/users/get-by-username?username={username}")
        else:
            raise InvalidParameters("No username or id provided")
        if user.status_code == 200:
            return User(self.requests, userid=user.json()["Id"])
        else:
            raise HTTPError(f"HTTP error occured with status code {str(user.status_code)}")

    def get_group(self, id=None):
        if id:
            return Group(self.requests, id)
        else:
            raise InvalidParameters("ID not provided")

    def get_game(self, id):
        return Game(self.requests, id)

    def get_trades(self, type="Inbound"):
        """
        Returns a list of trades.
        Available trade types:
        - Inbound
        - Outbound
        - Completed
        - Inactive
        """
        r = self.requests.get(f"https://trades.roblox.com/v1/trades/{type}")
        trades = []
        for trade in r.json()["data"]:
            trades.append(Trade(self.requests, trade["id"]))
        return trades

    def update_description(self, description=None):
        """
        Updates your description
        """
        if description:
            data = {
                "description": description
            }
            r = self.requests.post("https://accountinformation.roblox.com/v1/description", data=json.dumps(data))
            if r.status_code == 200:
                return True
            else:
                raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def get_trade(self, id=None):
        """
        Returns a Trade object, currently you can only get a trade by its ID.
        """
        return Trade(self.requests, id)
    
    def messages(self, PageNumber=0, PageSize=50, Tab="Inbox"):
        """
        Gets a list of messages either in your inbox or messages you've sent.
        """
        r = self.requests.get(f"https://privatemessages.roblox.com/v1/messages?pageNumber={str(PageNumber)}&pageSize={str(PageSize)}&messageTab={Tab}")
        messages = []
        if r.status_code == 200:
            for message in r.json()["collection"]:
                messages.append(Message(self.requests, message["subject"], message["body"], message["sender"]["id"], message["isSystemMessage"], message["isRead"]))
            return messages
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def get_gamepass(self, id):
        """
        Returns a Gamepass object of the specified gamepass
        """
        r = self.requests.get(f"https://api.roblox.com/marketplace/game-pass-product-info?gamePassId={str(id)}")
        data = r.json()
        if r.status_code == 200:
            return Gamepass(self.requests, data["TargetId"], data["Description"], data["Name"], data["ProductId"], data["PriceInRobux"], data["Creator"]["Id"])
        elif r.status_code == 500:
            raise InternalError(f"Invalid ID {str(id)}")
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")



    def friends(self):
        """
        Returns a list of friends the account has.
        """
        r = self.requests.get(f"https://friends.roblox.com/v1/users/{str(self.id)}/friends").json()
        if r.status_code == 200:
            friends = []
            for user in r["data"]:
                friends.append(User(self.requests, userid=user["id"]))
            return friends
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def friendrequests(self):
        """
        Returns a list of friend requests that the authenticated user has.
        Note that this will only return the first 100 friend requests you have.
        """
        r = self.requests.get("https://friends.roblox.com/v1/my/friends/requests?limit=100").json()
        friendrequests = []
        for user in r["data"]:
            friendrequests.append(FriendRequest(self.requests, userId=user["id"], account=self.id))
        return friendrequests

    def robux(self):
        """
        Amount of robux you currently have
        """
        r = self.requests.get(f"https://economy.roblox.com/v1/users/{str(self.id)}/currency")
        return r.json()["robux"]