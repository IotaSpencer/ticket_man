import discord
from discord.ext.pages import Page, Paginator

from ticket_man.bot.helpers.db_abbrevs import close_ticket, delete_ticket, get_all_open_tickets, open_ticket
from ticket_man.loggers import logger
from ticket_man.config import Configs

client = discord.Client()

class TicketsRefreshButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.danger, label='Refresh', emoji='♻', custom_id='refresh')

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        pages = []
        tickets = await get_all_open_tickets()
        for ticket in tickets:
            pages.append(Page(embeds=[make_embed(ticket)], custom_view=make_view(ticket)))

        paginator = Paginator(pages=pages)
        await paginator.respond(interaction)
        await interaction.delete_original_message(delay=3.0)
        await interaction.followup.send('Refreshed!', ephemeral=True, delete_after=5)


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
        ticket_id = kwargs.pop('ticket_id', None)
        custom_id = str(ticket_id) + '_close_button'
        self.ticket_id = ticket_id
        super().__init__(style=discord.ButtonStyle.danger, label='Close', emoji='🔒', custom_id=custom_id, *args,
                         **kwargs)

    async def callback(self, interaction: discord.Interaction):
        await interaction.delete_original_message(delay=2.0)
        ticket = await close_ticket(self.ticket_id)
        return await interaction.response.send_message(f"Ticket {ticket.id} closed", ephemeral=True)


class TicketOpenButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        custom_id = str(kwargs.pop('ticket_id', None)) + '_reopen_button'
        self.ticket_id = kwargs.pop('ticket_id', None)
        super().__init__(style=discord.ButtonStyle.danger, label='Reopen', emoji='🔓', custom_id=custom_id, *args,
                         **kwargs)

    async def callback(self, interaction: discord.Interaction):
        ticket = await open_ticket(self.ticket_id)
        await interaction.response.send_message(f"Ticket {ticket.id} reopened", ephemeral=True)
        await interaction.delete_original_message(delay=2.0)
        return ticket


def make_embed(ticket):
    last_updated_by_id = ticket.last_updated_by_id
    await discord.Bot.get_or_fetch_user(last_updated_by_id)
    embed = discord.Embed(title=f"Ticket {ticket.id}", color=0x00ff00)
    embed.add_field(name="Ticket ID", value=f"{ticket.id}", inline=False)
    embed.add_field(name="Ticket Status (open-1/closed-0)", value=f"{ticket.open}", inline=False)
    embed.add_field(name="Ticket Author", value=f"{ticket.user_id}", inline=False)
    embed.add_field(name="Ticket Subject", value=f"{ticket.subject}", inline=False)
    embed.add_field(name="Ticket Content", value=f"{ticket.content}", inline=False)
    embed.add_field(name="Ticket Created", value=f"{discord.utils.format_dt(ticket.created, 'F')}", inline=False)
    embed.add_field(name="Ticket Last Updated", value=f"{discord.utils.format_dt(ticket.last_updated, 'F')}", inline=False)
    embed.add_field(name="Ticket Last Updated By", value=f"{ticket.last_updated_by}", inline=False)

    return embed


def make_view(ticket):
    view = discord.ui.View()
    view.add_item(TicketsRefreshButton())
    view.add_item(TicketCloseButton(ticket_id=ticket.id))
    view.add_item(TicketDeleteButton(ticket_id=ticket.id))
    view.add_item(TicketOpenButton(ticket_id=ticket.id))
    return view
