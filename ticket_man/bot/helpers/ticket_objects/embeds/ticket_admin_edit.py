import discord
from discord import Button

from ticket_man.bot.helpers.ticket_objects.base_embed import EmbedBase


class AdminEditTicketEmbed(EmbedBase):
    def __init__(self, *args, **kwargs):
        ticket_id = kwargs.pop('ticket_id', None)
        super().__init__(*args, **kwargs)

    def get_buttons(self):
        buttons = []
        for klass in [TicketDeleteButton, TicketCloseButton, TicketReopenButton]:
            buttons += klass


class TicketDeleteButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.style = discord.ButtonStyle.danger
        self.label = 'Delete'
        self.emoji = '❌'
        self.custom_id = kwargs.pop('ticket_id', None) + '_delete_button'


class TicketCloseButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.style = discord.ButtonStyle.danger
        self.label = 'Close'
        self.emoji = '🔒'
        self.custom_id = kwargs.pop('ticket_id', None) + '_close_button'


class TicketReopenButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.style = discord.ButtonStyle.danger
        self.label = 'Reopen'
        self.emoji = '🔓'
        self.custom_id = kwargs.pop('ticket_id', None) + '_reopen_button'
