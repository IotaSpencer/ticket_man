import discord
from discord.ext.pages import Page, Paginator

from ticket_man.bot.helpers.db_abbrevs import close_ticket, delete_ticket, get_all_open_tickets, open_ticket
from ticket_man.bot.helpers.discord_helpers import user_distinct
from ticket_man.loggers import logger
from ticket_man.config import Configs


class TicketButtonsView(discord.ui.View):
    def __init__(self, ticket_id):
        super().__init__(timeout=20)
        self.ticket_id = ticket_id
        self.add_item(TicketCloseButton(ticket_id=ticket_id))
        self.add_item(TicketDeleteButton(ticket_id=ticket_id))
        self.add_item(TicketOpenButton(ticket_id=ticket_id))

    async def on_timeout(self) -> None:
        logger.debug(f"TicketButtonsView timed out for ticket {self.ticket_id}")
        await self.message.delete()

class TicketsRefreshButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.danger, label='Refresh', emoji='♻', custom_id='refresh')

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        pages = []
        tickets = await get_all_open_tickets()
        for ticket in tickets:
            pages.append(Page(embeds=[await make_embed(ticket)], custom_view=make_view(ticket)))

        paginator = Paginator(pages=pages)
        await paginator.respond(interaction)
        await interaction.delete_original_message(delay=3.0)
        await interaction.followup.send('Refreshed!', ephemeral=False, delete_after=5)


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
        await interaction.delete_original_response(delay=2.0)
        fticket = close_ticket(self.ticket_id)
        ticket = fticket.one()
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


async def make_embed(ticket, **kwargs):
    bot: discord.Bot = kwargs.get('bot', None)
    if bot is None:
        raise ValueError('Bot is required to make embed')
    last_updated_by_id = ticket.last_updated_by
    last_updated_by_user = await bot.get_or_fetch_user(last_updated_by_id)
    ticket_author_user = await bot.get_or_fetch_user(ticket.user_id)
    embed = discord.Embed(title=f"Ticket {ticket.id}", color=0x00ff00)
    embed.add_field(name="Ticket ID", value=f"{ticket.id}", inline=False)
    embed.add_field(name="Ticket Status (open-1/closed-0)", value=f"{ticket.open}", inline=False)
    embed.add_field(name="Ticket Author", value=f"{ticket.user_id} ({user_distinct(ticket_author_user)})", inline=False)
    embed.add_field(name="Ticket Subject", value=f"{ticket.subject}", inline=False)
    embed.add_field(name="Ticket Content", value=f"{ticket.content}", inline=False)
    embed.add_field(name="Ticket Created", value=f"{discord.utils.format_dt(ticket.created, 'F')}", inline=False)
    embed.add_field(name="Ticket Last Updated", value=f"{discord.utils.format_dt(ticket.last_updated, 'F')}",
                    inline=False)
    embed.add_field(name="Ticket Last Updated By",
                    value=f"{ticket.last_updated_by} ({user_distinct(last_updated_by_user)})", inline=False)

    return embed


def make_view(ticket):
    view = TicketButtonsView(ticket_id=ticket.id)
    return view
