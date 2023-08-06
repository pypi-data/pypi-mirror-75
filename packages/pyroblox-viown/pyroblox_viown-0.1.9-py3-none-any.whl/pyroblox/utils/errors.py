class AuthenticationFailed(Exception):
    """
    Authentication for the account has failed  
    when this is raised check that you've provided the correct .ROBLOSECURITY.
    """
    pass


class CookieNotProvided(Exception):
    """
    When you didn't provide a .ROBLOSECURITY for logging in
    """
    pass


class InvalidParameters(Exception):
    """
    The parameters you've provided is incorrect
    """
    pass


class HTTPError(Exception):
    """
    This error is usually thrown when a status code that isn't 2xx is returned.
    """
    pass


class InvalidFilterType(Exception):
    """
    This error is raised when you tried to filter by an invalid filter type.
    """
    pass


class AttributeNotFound(Exception):
    """
    This error is thrown when an attribute that doesn't exist has been accessed.  
    This error is no longer used
    """
    pass

class InvalidTrade(Exception):
    """
    When the trade that you tried to send is invalid  
    When this error occurs, it could be because:  
    - You offered more than 4 items / requested more than 4 items
    - You tried to offer more robux than you had
    - Item isn't in your inventory / Item isn't in your targets inventory
    - User you tried to trade with has trades closed
    - Lowball filter activated
    """
    pass


class PurchaseError(Exception):
    """When a purchase attempt fails"""
    pass


class InternalError(Exception):
    """When an internal error occurs"""
    pass


class PermissionError(Exception):
    """When you don't have the permissions to complete the action"""
    pass


class CaptchaError(Exception):
    """
    This error is raised when a request requires a captcha token, since these can't be ignored, this error is thrown instead
    """
    pass