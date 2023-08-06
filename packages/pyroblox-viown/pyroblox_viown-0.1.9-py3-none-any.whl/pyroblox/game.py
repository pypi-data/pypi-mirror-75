import json
from .server import Server
from .gamepass import Gamepass
from .utils.errors import HTTPError

class Game:
    def __init__(self, requests, gameId):
        """
        Represents a game object
        """
        self.requests = requests
        self.id = gameId
        """ID of the game"""
    
    def _UniverseID(self):
        """
        For getting the UniverseID of the game  
        This is mainly used by pyroblox
        """
        r = self.requests.get(f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={str(self.id)}").json()
        return r[0]["universeId"]

    def servers(self, page=1):
        """
        Returns a list of servers of the game
        """
        r = self.requests.get(f"https://www.roblox.com/games/getgameinstancesjson?placeId={str(self.id)}&startIndex=0")
        if r.status_code == 200:
            servers = []
            for server in r.json()["Collection"]:
                servers.append(Server(server["Ping"], server["Fps"], server["Guid"], server["PlaceId"], server["ShowSlowGameMessage"]))
            return servers
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")


    def information(self):
        """
        Returns a dictionary of information about the game
        """
        r = self.requests.get(f"https://games.roblox.com/v1/games?universeIds={str(self.id)}")
        if r.status_code == 200:
            return r.json()
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")
        

    def like(self):
        """
        Likes the game
        """
        r = self.requests.post(f"https://www.roblox.com/voting/vote?assetId={str(self.id)}&vote=true")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def dislike(self):
        """
        Dislikes the game
        """
        r = self.requests.post(f"https://www.roblox.com/voting/vote?assetId={str(self.id)}&vote=false")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def favorite(self):
        """
        Favorites a game  
        This method works as a toggle, running it will favorite the game, running it one more time will unfavorite the game
        """
        data = {
            "assetID": self.id
        }
        r = self.requests.post(f"https://www.roblox.com/favorite/toggle", data=json.dumps(data))
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def gamepasses(self):
        """
        Returns a list of gamepass objects from the game
        """
        r = self.requests.get(f"https://games.roblox.com/v1/games/{self._UniverseID()}/game-passes")
        gamepasses = []
        for gamepass in r.json()["data"]:
            extraInfo = self.requests.get(f"https://api.roblox.com/marketplace/game-pass-product-info?gamePassId={gamepass['id']}").json()
            gamepasses.append(Gamepass(self.requests, gamepass["id"], "None", gamepass["name"], gamepass["productId"], gamepass["price"], extraInfo["Creator"]["Id"]))
        return gamepasses

    def favorites(self):
        """
        Returns the amount of favorites the game has
        """
        r = self.requests.get(f"https://games.roblox.com/v1/games/{self._UniverseID()}/favorites/count")
        return r.json()["favoritesCount"]

    def create_vipserver(self):
        """
        Creates a vip server for the game  
        WARNING: Some VIP servers cost robux, running this method may cause you to lose robux.
        """
        pass