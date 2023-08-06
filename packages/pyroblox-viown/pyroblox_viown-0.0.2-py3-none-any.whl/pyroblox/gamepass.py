from .utils.errors import OffsaleError

class Gamepass:
    def __init__(self, id, name, productId, price):
        """
        Represents a gamepass object  
        """
        self.id = id
        """The ID of the gamepass"""
        self.name = name
        """The name of the gamepass"""
        self.productId = productId
        """The ProductId of the gamepass"""
        self.price = price or -1
        """Price of the gamepass (in robux), this will return -1 if the gamepass is offsale."""

    def buy(self):
        """
        Purchases the gamepass  
        WARNING: This will spend robux from the authenticated user
        """
        if self.price == -1:
            raise OffsaleError("Gamepass is offsale and cannot be bought")