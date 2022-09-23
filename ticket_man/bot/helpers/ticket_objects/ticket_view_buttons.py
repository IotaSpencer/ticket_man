import discord

from ticket_man.bot.helpers.db_abbrevs import close_ticket, delete_ticket, open_ticket
from ticket_man.loggers import logger


class TicketDeleteButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        self.ticket_id = kwargs.pop('ticket_id')
        custom_id = f'ticket_{self.ticket_id}_delete_button'
        super().__init__(style=discord.ButtonStyle.danger, label='Delete', emoji='❌', custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message('Ticket deleted', ephemeral=True)
        logger.info(
            f"Ticket {self.ticket_id} deleted by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})")
        await delete_ticket(self.ticket_id)
        await interaction.delete_original_message(delay=2.0)


class TicketCloseButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        custom_id = str(kwargs.pop('ticket_id', None)) + '_close_button'
        super().__init__(style=discord.ButtonStyle.danger, label='Close', emoji='🔒', custom_id=custom_id, *args,
                         **kwargs)
        self.ticket_id = kwargs.pop('ticket_id', None)

    async def callback(self, interaction: discord.Interaction):
        await interaction.delete_original_message(delay=2.0)
        ticket = await close_ticket(self.ticket_id)
        return await interaction.response.send_message(f"Ticket {ticket.id} closed", ephemeral=True)


class TicketOpenButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        custom_id = str(kwargs.pop('ticket_id', None)) + '_reopen_button'
        super().__init__(style=discord.ButtonStyle.danger, label='Reopen', emoji='🔓', custom_id=custom_id, *args,
                         **kwargs)
        self.ticket_id = kwargs.pop('ticket_id', None)

    async def callback(self, interaction: discord.Interaction):
        ticket = await open_ticket(self.ticket_id)
        await interaction.response.send_message(f"Ticket {ticket.id} reopened", ephemeral=True)
        await interaction.delete_original_message(delay=2.0)
        return ticket
