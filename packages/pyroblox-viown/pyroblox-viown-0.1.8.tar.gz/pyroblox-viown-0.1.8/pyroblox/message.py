from .user import User

class Message:
    def __init__(self, requests, subject=None, body=None, authorId=1, isSystem=False, isRead=False):
        """
        Represents a message object
        """
        self.requests = requests
        self.subject = subject
        """The subject of the message"""
        self.body = body
        """The content of the message"""
        self.authorId = authorId
        self.isread = isRead
        """Whether or not the message is marked as read"""
        self.issystem = isSystem
        """Whether or not this is a system message"""

    def author(self):
        """
        Returns a User object that represents who wrote the message
        """
        return User(self.requests, userid=self.authorId)

    def mark_read(self):
        """
        Marks a message as read
        """
        pass

    def mark_unread(self):
        """
        Marks a message as unread
        """
        pass

    def archive(self):
        """
        Archives the message
        """
        pass

    def unarchive(self):
        """
        Unarchives the message
        """
        pass