# built-in

# 3rd party
from discord.ext.commands import Cog, command
from discord.commands import slash_command
# local
from ticket_man.loggers import logger


class Tickets(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.tickets'

    @slash_command(name="ticket")
    async def ticket(self, ctx):
        pass




def setup(bot):
    bot.add_cog(Tickets(bot))
    logger.info('Loaded Tickets')


def teardown(bot):
    bot.remove_cog(Tickets(bot))
    logger.info('Unloaded Tickets')
