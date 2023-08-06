from ..utils.functions import Functions
from ..user import User

functions = Functions()

class Wallpost:
    def __init__(self, requests, group, body=None, groupId=None, postId=None, username=None, userid=None, created=None, updated=None):
        """
        Represents a post on a group wall
        """
        self.requests = requests
        self.body = body
        """The posts body"""
        self.postid = postId
        """The ID of the post"""
        self.groupid = groupId
        """The ID of the group"""
        self.userid = userid
        self.author = User(self.requests, self.userid)
        """Returns a User object of the person who submitted the post"""
        self.created = functions.dateconvert(created)
        """Date the post was created (datetime.datetime)"""
        self.updated = functions.dateconvert(updated)
        """Date the post was updated (datetime.datetime)"""
        self.group = group(self.requests, self.groupid)
        """Returns a Group object of the group the wallpost was posted in"""

    def delete(self):
        """
        Deletes the wall post  

        The `Delete group wall posts` permission is required for this action
        """
        r = self.requests.delete(f"https://groups.roblox.com/v1/groups/{str(self.groupid)}/wall/posts/{str(self.postid)}")
        if r.status_code == 200:
            return True
        elif r.status_code == 403:
            raise PermissionError("You do not have the appropriate permissions for this action")
        else:
            raise HTTPError(f"Request failed with status code {r.status_code}")