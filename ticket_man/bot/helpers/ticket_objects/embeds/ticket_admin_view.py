import discord
from discord import Button
from discord.ui import Item

from ticket_man.bot.helpers.db_abbrevs import get_ticket
from ticket_man.bot.helpers.ticket_objects.base_embed import EmbedBase


class AdminViewTicketEmbedView(discord.ui.View):
    def __init__(self, *items: Item):
        super().__init__(*items)


class AdminViewTicketEmbed(EmbedBase):
    def __init__(self, *args, **kwargs):
        ticket_id = kwargs.pop('ticket_id', None)
        super().__init__(*args, **kwargs)

    def view(self, ticket_id):
        return AdminViewTicketEmbedView(TicketDeleteButton(ticket_id=ticket_id), TicketCloseButton(ticket_id=ticket_id),
                                        TicketOpenButton(ticket_id=ticket_id))


class TicketDeleteButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = discord.ButtonStyle.danger
        self.ticket_id = kwargs.pop('ticket_id', None)
        self.label = 'Delete'
        self.emoji = '❌'
        self.custom_id = kwargs.pop('ticket_id', None) + '_delete_button'


class TicketCloseButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.style = discord.ButtonStyle.danger
        self.ticket_id = kwargs.pop('ticket_id', None)
        self.label = 'Close'
        self.emoji = '🔒'
        self.custom_id = kwargs.pop('ticket_id', None) + '_close_button'

    def callback(self, interaction: discord.Interaction):
        open_ticket = await get_ticket(self.ticket_id)


class TicketOpenButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.style = discord.ButtonStyle.danger
        self.ticket_id = kwargs.pop('ticket_id', None)
        self.label = 'Reopen'
        self.emoji = '🔓'
        self.custom_id = kwargs.pop('ticket_id', None) + '_reopen_button'
