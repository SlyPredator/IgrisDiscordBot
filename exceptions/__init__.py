from discord.ext import commands


class UserBlacklisted(commands.CheckFailure):
    """
    Thrown when a user is attempting something, but is blacklisted.
    """

    def __init__(self, message="User is blacklisted!"):
        self.message = message
        super().__init__(self.message)


class UserNotOwner(commands.CheckFailure):
    """
    Thrown when a user is attempting something, but is not an owner of the bot.
    """

    def __init__(self, message="User is not an owner of the bot!"):
        self.message = message
        super().__init__(self.message)


class UserNotModerator(commands.CheckFailure):
    """
    Thrown when a user is attempting something, but it not a moderator of the bot.
    """

    def __init__(self, message="User is not a moderator of the bot!"):
        self.message = message
        super().__init__(self.message)
