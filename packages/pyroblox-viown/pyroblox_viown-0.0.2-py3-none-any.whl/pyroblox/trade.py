from .utils.errors import HTTPError, InvalidTrade
from .tradeinformation import TradeInformation

class Trade:
    def __init__(self, requests, tradeId):
        """
        Represents a trade object
        """
        self.requests = requests
        self.id = tradeId
        """ID of the trade"""
        self.information = TradeInformation(self.requests, self.id)
        """A TradeInformation object for the trade"""
        

    def accept(self):
        """
        Accepts the roblox trade  
        WARNING: This will fail on outbound/inactive/completed trades.
        """
        r = self.requests.post(f"https://trades.roblox.com/v1/trades/{str(self.id)}/accept")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")

    def decline(self):
        """
        Declines the trade  
        WARNING: This will fail on inactive/completed trades.
        """
        r = self.requests.post(f"https://trades.roblox.com/v1/trades/{str(self.id)}/decline")
        if r.status_code == 200:
            return True
        else:
            raise HTTPError(f"HTTP error occured with status code {str(r.status_code)}")