import requests
from .utils.errors import CookieNotProvided, AuthenticationFailed
from .account import Account


class Login:
    def __init__(self, cookie=None):
        """
        For authentication, currently you can only login through the .ROBLOSECURITY cookie.
        If you don't know how to get your .ROBLOSECURITY, you can use this extension: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en
        """
        self.requests = requests.Session()
        self.authenticated = False
        self.userid = 0
        """UserId of your account"""
        self.cookie = cookie
        """Your .ROBLOSECURITY cookie"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://www.roblox.com',
            'X-CSRF-TOKEN': self._get_token(cookie),
            'DNT': '1'
        }
        if cookie:
            r = self._login(cookie)
            if r:
                self.userid = r
                self.authenticated = True
        else:
            raise CookieNotProvided(".ROBLOSECURITY was not provided")
        self.account = Account(self.requests, self.userid)
        """The Account class for the user, this can be used to wear items, change status, etc"""


    def _login(self, cookie):
        """
        Mainly used by pyroblox to verify cookies.
        """
        r = self.requests.get(
            "https://www.roblox.com/game/GetCurrentUser.ashx", cookies={".ROBLOSECURITY": cookie})
        if r.text == 'null':
            raise AuthenticationFailed("Invalid .ROBLOSECURITY")
        else:
            self.requests.cookies[".ROBLOSECURITY"] = cookie
            self.requests.headers = self.headers
            return int(r.text)


    def _get_token(self, cookie):
        """
        Gets the X-CSRF token, this is mainly used by pyroblox, you shouldn't worry about this.
        """
        r = requests.post("https://friends.roblox.com/v1/users/1/follow",
                          cookies={".ROBLOSECURITY": cookie})
        return r.headers['x-csrf-token']
