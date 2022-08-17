import omegaconf.errors
from discord.ext.commands import CommandError, CheckFailure
from discord import ApplicationCommandError


class ConfirmPermError(CheckFailure):
    pass


class HelperPermError(CheckFailure):
    pass


class NoAttachmentError(CheckFailure):
    pass


class TooManyAttachmentError(CheckFailure):
    pass


class NoGuildInContextError(CheckFailure):
    pass


class GuildNotInDBError(omegaconf.errors.ConfigKeyError):
    pass


class NoGuildArgError(CheckFailure):
    pass


class NoUsersToPurgeError(CommandError, ApplicationCommandError):
    pass
