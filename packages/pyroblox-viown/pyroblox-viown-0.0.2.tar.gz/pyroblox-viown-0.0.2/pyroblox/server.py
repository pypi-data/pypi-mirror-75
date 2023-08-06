class Server:
    def __init__(self, ping : int, fps : int, jobid : str, placeid : int, isSlow : bool):
        """
        Represents a roblox server.
        """
        self.ping = ping
        """Server's ping"""
        self.fps = fps
        """Server's FPS"""
        self.jobid = jobid
        """JobID of the server"""
        self.placeid = placeid
        """PlaceID of the server"""
        self.players = []
        """A list of players in the server.  
        WARNING: Due to Roblox updates, you're no longer allowed to view the players in the server"""
        self.slow = isSlow
        """Whether or not the server is in the `slow` state or not"""