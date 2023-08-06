from ..utils.errors import PermissionError, HTTPError
from ..user import User

class JoinRequest:
    def __init__(self, requests, userId=None, username=None, created=None):
        """
        Represents a group member join request
        """
        self.requests = requests
        self.id = userId
        """The ID of the user"""
        self.username = username
        """The username of the user"""
        self.created = created
        """The date they joined  
        As of right now this returns a string and not a datetime object, this will change soon"""

    def user(self):
        """
        Returns the User object for the requester
        """
        return User(self.requests, self.id)

    def accept(self):
        """
        Accepts the join request
        """
        r = self.requests.post(f"https://groups.roblox.com/v1/groups/7302938/join-requests/users/{str(self.id)}")
        if r.status_code == 200:
            return True
        elif r.status_code == 403:
            raise PermissionError("You do not have the appropriate permissions for this action")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")

    def decline(self):
        """
        Declines the join request
        """
        r = self.requests.delete(f"https://groups.roblox.com/v1/groups/7302938/join-requests/users/{str(self.id)}")
        if r.status_code == 200:
            return True
        elif r.status_code == 403:
            raise PermissionError("You do not have the appropriate permissions for this action")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")