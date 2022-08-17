# built-in
# 3rd party
# local
from discord.ext.commands import check

from .discord_helpers import *
from ...exceptions import ConfirmPermError, HelperPermError


def confirmable_check():
    def predicate(ctx):
        if has_server_confirm_role(ctx.guild, ctx.author):
            return True
        else:
            raise ConfirmPermError
    return check(predicate)

def helper_check():
    def predicate(ctx):
        if has_server_helper_role(ctx.guild, ctx.author):
            return True
        else:
            raise HelperPermError
    return check(predicate)