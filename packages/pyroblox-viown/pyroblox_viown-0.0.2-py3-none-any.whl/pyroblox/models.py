from .login import Login
from .item import Item
from .account import Account
from .trade import Trade
from .tradeinformation import TradeInformation
from .user import User
from .message import Message

class Models:
    def __init__(self):
        """
        Model classes.
        This can be used to instantiate your own pyroblox classes.
        """
        self.login = Login
        """Returns an instance of the Login class"""
        self.item = Item
        """Returns an instance of the Item class"""
        self.account = Account
        """Returns an instance of the Account class"""
        self.trade = Trade
        """Returns an instance of the Trade class"""
        self.tradeinformation = TradeInformation
        """Returns an instance of the TradeInformation class"""
        self.user = User
        """Returns an instance of the User class"""
        self.message = Message
        """Returns an instance of the Message class"""