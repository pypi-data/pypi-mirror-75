from .user import User
from .utils.errors import HTTPError

class FriendRequest:
    def __init__(self, requests, userId=None, account=None):
        """
        Represents a FriendRequest object
        """
        self.id = userId
        """The id of the user"""
        self.requests = requests
        self.account = account
        self.user = User(self.requests, userid=self.id)
        """Returns a User object of the user"""

    def accept(self):
        """
        Accepts the friend request
        """
        r = self.requests.post(f"https://friends.roblox.com/v1/users/{str(self.id)}/accept-friend-request")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def decline(self):
        """
        Declines the friend request
        """
        r = self.requests.post(f"https://friends.roblox.com/v1/users/{str(self.id)}/decline-friend-request")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")