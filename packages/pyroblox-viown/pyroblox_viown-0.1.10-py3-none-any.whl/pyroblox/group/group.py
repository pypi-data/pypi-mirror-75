from ..utils.errors import PermissionError, HTTPError
from ..game import Game

from .joinrequest import JoinRequest
from .wallpost import Wallpost
from .member import Member


class Group:
    def __init__(self, requests, groupId=None):
        """
        Represents a group object  
        As of right now this class is not complete.
        """
        self.requests = requests
        self.id = groupId

    def joinrequests(self):
        """
        Gets a list of join requests in the group  
        Returns a list of JoinRequest objects  

        The `Accept Join Requests` permission is required for this action
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/join-requests")
        if r.status_code == 200:
            requests = []
            for joinrequest in r.json()["data"]:
                requests.append(JoinRequest(self.requests, joinrequest["requester"]["userId"], joinrequest["requester"]["username"], joinrequest["created"]))
            return requests
        elif r.status_code == 403:
            raise PermissionError("You do not have the appropriate permissions for this action")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")


    def games(self):
        """
        Returns a list of games the group has created
        """
        r = self.requests.get(f"https://games.roblox.com/v2/groups/{str(self.id)}/games")
        gameslist = []
        for game in r.json()["data"]:
            gameslist.append(Game(self.requests, game["id"]))
        return gameslist


    def members(self):
        """
        Returns a list of members in the group  

        Returns a list of Member objects
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/users")
        userslist = []
        for user in r.json()["data"]:
            userslist.append(Member(self.requests, user["user"]["userId"], user["user"]["username"], user["role"]["id"], user["role"]["name"], user["role"]["rank"]))
        return userslist

    def wall(self):
        """
        Returns the last 50 messages posted on the group wall  
        Returns a list of Wallpost objects  

        The `View Group Wall` permission is required for this action
        """
        r = self.requests.get(f"https://groups.roblox.com/v1/groups/{str(self.id)}/wall/posts?limit=50")
        wallposts = []
        for post in r.json()["data"]:
            wallposts.append(Wallpost(self.requests, Group, post["body"], self.id, post["id"], post["poster"]["username"], post["poster"]["userId"], post["created"], post["updated"]))
        return wallposts

    def set_role_by_rank(self, id=None, username=None, rankid=None):
        """
        Sets the member's role by the rank  

        The `Manage lower-ranked member ranks` permission is required for this action
        """
        pass

    def set_role(self, id=None, username=None, roleid=None):
        """
        Sets the member's role by the role's name  

        The `Manage lower-ranked member ranks` permission is required for this action  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def funds(self):
        """
        Returns the amount of funds in the group  

        The group funds have to be public or you must have access to them to run this method  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def allies(self):
        """
        Returns a list of allies the group has  

        Returns a list of Group objects  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def enemies(self):
        """
        Returns a list of enemies the group has  

        Returns a list of Group objects  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def auditlog(self):
        """
        Returns the first 100 logs in the audit log  

        The `View audit log` permission is required for this action  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def shout(self):
        """
        Performs a shout in the group  

        The `Post group shout` permission is required for this action  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def get_shout(self):
        """
        Returns a Groupshout object representing the current shout message  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def roles(self):
        """
        Returns a list of roles the group has    
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def creator(self):
        """
        Returns a User object of who owns the group  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def payout(self, id=None, username=None, amount=None):
        """
        Sends a group payout to the specified user  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass

    def exile(self, id=None, username=None):
        """
        Exiles a user from the group  

        The `Kick lower-ranked members` permission is required for this action  
        THIS METHOD IS CURRENTLY NOT COMPLETE
        """
        pass