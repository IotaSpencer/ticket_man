# built-in
from discord import ApplicationContext
# 3rd party
from discord.ext.commands import Cog, command
from discord.commands import slash_command
# local
from ticket_man.loggers import logger
from ticket_man.bot.helpers.modals import MyModal, TicketSubmitView
from ticket_man.bot.helpers.db_abbrevs import get_ticket_type


class Tickets(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.tickets'

    @slash_command(name="ticket")
    async def ticket(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)
        await ctx.respond(view=TicketSubmitView())


def setup(bot):
    bot.add_cog(Tickets(bot))
    logger.info('Loaded Tickets')


def teardown(bot):
    bot.remove_cog(Tickets(bot))
    logger.info('Unloaded Tickets')
