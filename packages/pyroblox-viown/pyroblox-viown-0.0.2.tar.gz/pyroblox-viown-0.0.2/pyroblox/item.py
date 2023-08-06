from .utils.errors import AttributeNotFound
import datetime

class Item:
    def __init__(self, assetName, userAssetId, assetId, RAP=None, ownerId=None, ownerName=None, created=None, updated=None):
        """
        Represents a roblox item
        """
        self.__createdDate = created
        self.__updatedDate = updated
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
        if created:
            self.created = self._created()
        if updated:
            self.updated = self._updated()


    def _created(self):
        """
        Date the item was created.
        This only works on user-created objects, this will return False on items created by Roblox.
        """
        if self.__createdDate:
            s = self.__createdDate.split('T')[0].split('-')
            return datetime.datetime(int(s[0]), int(s[1]), int(s[2]))
        else:
            return False

    def _updated(self):
        """
        Date the item was updated.
        This only works on some items
        """
        if self.__updatedDate:
            s = self.__updatedDate.split('T')[0].split('-')
            return datetime.datetime(int(s[0]), int(s[1]), int(s[2]))
        else:
            return False