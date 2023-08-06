from ..user import User

class Member:
    def __init__(self, requests, userId=None, username=None, roleId=None, roleName=None, rank=None):
        """
        Represents a group member object
        """
        self.requests = requests
        self.id = userId
        """The ID of the user"""
        self.user = User(self.requests, self.id)
        """Returns the User object of the user"""
        self.roleid = roleId
        """The ID of the role (not the rank)"""
        self.rolename = roleName
        """The name of the role"""
        self.rank = rank
        """The rank of the user (1-255)"""