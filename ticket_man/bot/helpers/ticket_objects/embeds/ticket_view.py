import discord


class ViewTicketView(discord.ui.View):
    def __init__(self, ticket: discord.Message):
        super().__init__()
        self.ticket = ticket
