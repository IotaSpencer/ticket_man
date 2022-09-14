import discord
from discord import Button

from ticket_man.bot.helpers.ticket_objects.embeds import EmbedBase


class AdminViewTicketEmbed(EmbedBase):
    def __init__(self, *args, **kwargs):
        ticket_id = kwargs.pop('ticket_id', None)
        super().__init__(*args, **kwargs)

    def get_buttons(self):
        buttons = []
        for klass in []:
            buttons += klass


class TicketDelete(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.style = discord.ButtonStyle.danger
        self.label = 'Delete'
        self.emoji = '❌'
        self.custom_id = kwargs.pop('ticket_id', None) + '_delete_button'
