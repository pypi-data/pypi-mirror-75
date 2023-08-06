import dateutil.parser

class Functions:
    def __init__(self):
        """
        A list of useful functions, mostly used by pyroblox
        """
        pass

    def dateconvert(self, utc):
        """
        Converts UTC string to a datetime.datetime object
        """
        return dateutil.parser.parse(utc)