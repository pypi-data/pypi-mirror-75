from .utils.errors import PurchaseError, HTTPError
from .user import User
import json

class Gamepass:
    def __init__(self, requests, id, description, name, productId, price, creatorId=0):
        """
        Represents a gamepass object  
        """
        self.requests = requests
        self.id = id
        """The ID of the gamepass"""
        self.name = name
        """The name of the gamepass"""
        self.description = description
        """The description of the product"""
        self.productid = productId
        """The ProductId of the gamepass"""
        self.price = price or -1
        """Price of the gamepass (in robux), this will return -1 if the gamepass is offsale."""
        self.creatorId = creatorId
        """ID of the creator"""
        
    def creator(self):
        """
        Returns a User object of the creator of the gamepass.  
        (A Group object is returned instead if the gamepass was by a group)
        """
        return User(self.requests, self.creatorId)

    def buy(self):
        """
        Purchases the gamepass
        """
        if self.price == -1:
            raise PurchaseError("Gamepass is offsale and cannot be bought")
        data = {
            "expectedPrice": self.price
        }
        r = self.requests.post(f"https://economy.roblox.com/v1/purchases/products/{self.productid}", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"Request failed, server returned {str(r.status_code)}")