# built-in

# 3rd party
from typing import Union

import tribool as tribool
from discord import ApplicationContext
from discord.ext.commands import Converter, Context


# local


async def is_server_owner(ctx: Union[Context, ApplicationContext]) -> bool | None:
    if ctx.guild:
        return ctx.author == ctx.guild.owner
    else:
        return None
