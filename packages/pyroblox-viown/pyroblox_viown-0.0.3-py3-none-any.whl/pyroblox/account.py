from .utils.errors import HTTPError
from .user import User
from .friendrequest import FriendRequest
from .message import Message
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

    def friends(self):
        """
        A list of friends you have
        """