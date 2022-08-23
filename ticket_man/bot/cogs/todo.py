# built-in function
import re

# 3rd party
import discord
from discord.ext import commands, bridge

# local
from ticket_man.loggers import logger
import ticket_man.db

class TODO(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.todo'

    @commands.group()
    @commands.is_owner()
    async def todo(self, ctx):
        pass

    @todo.command()
    @commands.is_owner()
    async def add(self, ctx, item):
        """Add a todo item"""
        pass

    @todo.command()
    @commands.is_owner()
    async def remove(self, ctx, num):
        """Remove a todo item"""
        pass

    @todo.command()
    @commands.is_owner()
    async def list(self, ctx):
        """List out todo items"""
        pass

    @todo.command()
    @commands.is_owner()
    async def set_increment(self, ctx, num):
        """Reset the increment back to NUM"""
        pass


def setup(bot):
    bot.add_cog(TODO(bot))
    logger.info('Loaded TODO')


def teardown(bot):
    bot.remove_cog(TODO(bot))
    logger.info('Unloaded TODO')
