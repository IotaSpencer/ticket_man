import discord
from . import EmbedBase


class ViewTicketEmbed(EmbedBase):
    def __init__(self, ticket: discord.Message):
        super().__init__()
        self.ticket = ticket
