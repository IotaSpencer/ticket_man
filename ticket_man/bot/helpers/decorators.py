from discord.ext import commands

from ticket_man.config import Configs


def is_valid_server_in_db(self):
    def predicate(ctx):
        in_discord = False
        in_db = False
        guild_id = ctx.message.content.split(' ')[1]  # may not be valid guild ID
        if ctx.get_guild("{}".format(guild_id)):  # see if exists on discord
            in_discord = True
        else:
            pass
        if guild_id in Configs.sdb.servers.keys():
            in_db = True
        else:
            pass

        return in_db and in_discord

    return commands.check(predicate)
