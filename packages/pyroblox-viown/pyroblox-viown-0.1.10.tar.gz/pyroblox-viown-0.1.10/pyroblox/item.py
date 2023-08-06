from .utils.errors import AttributeNotFound
from .utils.functions import Functions
import datetime

functions = Functions()

class Item:
    def __init__(self, assetName, userAssetId, assetId, RAP=None, ownerId=None, ownerName=None, created=None, updated=None):
        """
        Represents a roblox item
        """
        # Properties
        self.name = assetName
        """Name of the item"""
        self.RecentAveragePrice = RAP
        self.rap = RAP or False
        """RAP of the item, returns False if the item does not have a RAP"""
        self.assetid = assetId
        """The ID of the asset"""
        self.userassetid = userAssetId
        """The UserAssetID of the item, this can be used in making trades. This is NOT the asset id of the item."""
        self.ownerid = ownerId
        """UserID of the player who owns the item"""
        self.ownername = ownerName
        """The name of the player who owns the item"""
        self.created = None
        """Date the item was created"""
        self.updated = None
        """Date the last time the item was updated"""
        if created:
            self.created = functions.dateconvert(created)
        if updated:
            self.updated = functions.dateconvert(updated)