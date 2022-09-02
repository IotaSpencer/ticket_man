# built-in
import asyncio
from pathlib import Path
import inspect
# 3rd party
import discord
from discord.errors import Forbidden
from discord.ext import commands, bridge
from discord import Member, TextChannel, slash_command

# local
from ticket_man.bot.helpers.decorators import *
from ticket_man.bot.helpers.discord_helpers import *
from ticket_man.loggers import logger
from ticket_man.config import Configs


class JoinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.join_message'

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        await asyncio.sleep(5)
        try:
            await member.send(
                f"Hello {member.mention}, welcome to {member.guild.name}! "
                f"\n\n"
                f"If you're here to submit a ticket, please see the #ticket-submit channel or use the {'/ticket'} command. "

            )
        except Forbidden:
            pass
            # If they can't be messaged, then fuck them.

    @slash_command(name="whoami")
    async def whoami(self, ctx):
        await ctx.send(f"{ctx.author.mention}")

def setup(bot):
    bot.add_cog(JoinMessage(bot))
    logger.info('Loaded JoinMessage')


def teardown(bot):
    bot.remove_cog(JoinMessage(bot))
    logger.info('Unloaded JoinMessage')
