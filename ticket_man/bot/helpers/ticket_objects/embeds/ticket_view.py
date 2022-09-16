import discord
from ticket_man.bot.helpers.ticket_objects.base_embed import EmbedBase


class ViewTicketEmbed(EmbedBase):
    def __init__(self, ticket: discord.Message):
        super().__init__()
        self.ticket = ticket
