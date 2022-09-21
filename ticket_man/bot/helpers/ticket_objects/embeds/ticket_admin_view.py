import discord
from discord import Button
from discord.ui import Item

from ticket_man.bot.helpers.db_abbrevs import close_ticket, delete_ticket, get_ticket, open_ticket
from ticket_man.bot.helpers.ticket_objects.base_embed import EmbedBase
from ticket_man.loggers import logger


class AdminViewTicketEmbedView(discord.ui.View):
    def __init__(self, *items: Item):
        super().__init__(*items)


class TicketDeleteButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        self.ticket_id = kwargs.pop('ticket_id')
        custom_id = f'ticket_{self.ticket_id}_delete_button'
        super().__init__(style=discord.ButtonStyle.danger, label='Delete', emoji='❌', custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message('Ticket deleted', ephemeral=True)
        logger.info(f"Ticket {self.ticket_id} deleted by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})")
        await delete_ticket(self.ticket_id)

class TicketCloseButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        custom_id = str(kwargs.pop('ticket_id', None)) + '_close_button'
        super().__init__(style=discord.ButtonStyle.danger, label='Close', emoji='🔒', custom_id=custom_id, *args,
                         **kwargs)
        self.ticket_id = kwargs.pop('ticket_id', None)

    async def callback(self, interaction: discord.Interaction):
        open_ticket = await close_ticket(self.ticket_id)


class TicketOpenButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        custom_id = str(kwargs.pop('ticket_id', None)) + '_reopen_button'
        super().__init__(style=discord.ButtonStyle.danger, label='Reopen', emoji='🔓', custom_id=custom_id, *args,
                         **kwargs)
        self.ticket_id = kwargs.pop('ticket_id', None)

    async def callback(self, interaction: discord.Interaction):
        ticket = await open_ticket(self.ticket_id)
