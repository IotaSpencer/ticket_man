# built-in function
import re

# 3rd party
import discord
from discord.ext import commands

# local
from ticket_man.loggers import logger


class Extensions(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.extensions'

    @commands.group(case_insensitive=True)
    async def ext(self, ctx):
        pass

    @ext.group()
    @commands.is_owner()
    async def cogs(self, ctx):
        pass

    @ext.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        ctx.bot.load_extension(extension)
        await ctx.reply('Loaded {}'.format(extension))

    @ext.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        ctx.bot.unload_extension(extension)
        await ctx.reply('Unloaded {}'.format(extension))

    @ext.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        ctx.bot.reload_extension(extension)
        await ctx.reply('Reloaded {}'.format(extension))

    ###########
    #
    # Only Cog extensions commands
    #
    ###########

    @cogs.command()
    async def reload_all(self, ctx):
        for cog_name, cog_class in ctx.bot.cogs.copy().items():
            if cog_class.ext_path != 'ticket_man.bot.cogs.extensions':
                ctx.bot.reload_extension(cog_class.ext_path)
        await ctx.reply("Reloaded all cogs.")


def setup(bot):
    bot.add_cog(Extensions(bot))
    logger.info('Loaded Extensions')


def teardown(bot):
    bot.remove_cog(Extensions(bot))
    logger.info('Unloaded Extensions')
