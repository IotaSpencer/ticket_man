# built-in

# 3rd party
from typing import Union

from discord import ApplicationContext
from discord.ext.commands import Converter, Context
# local

from . import discord_helpers, info_embeds, decorators
from . import wait_fors


async def is_server_owner(ctx: Union[Context, ApplicationContext]):
    return ctx.author.id == ctx.guild.owner_id
