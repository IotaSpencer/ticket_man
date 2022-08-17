# built-in function
import re

# 3rd party
import discord
from discord.ext import commands, bridge

# local
from ticket_man.loggers import logger


class TODO(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.todo'

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.close()
        await ctx.bot.loop.close()


def setup(bot):
    bot.add_cog(TODO(bot))
    logger.info('Loaded TODO')


def teardown(bot):
    bot.remove_cog(TODO(bot))
    logger.info('Unloaded TODO')
