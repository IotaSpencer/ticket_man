from discord.ext import commands


###
#
# todo - add -
#
# content
# priority
# completed
#
###
class TodoAddFlags(commands.FlagConverter):
    content: str
    priority: int = 1
    completed: bool = False
