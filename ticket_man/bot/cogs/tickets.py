# built-in
import datetime
# 3rd party
import arrow as arw
import discord.ui
from discord.cog import Cog
from discord.commands import SlashCommandGroup
from discord import ApplicationContext, Embed, Permissions, default_permissions
from discord.ext.pages import Page, Paginator

from ticket_man.bot.helpers.db_abbrevs import add_test_tickets, close_ticket, get_all_open_tickets, get_ticket, \
    open_ticket

# local
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_comment import CommentTicketView
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_submit import TicketSubmitView
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_view import ViewTicketEmbed
from ticket_man.bot.helpers.ticket_objects.make_pages import TicketCloseButton, TicketDeleteButton, make_embed, make_view
from ticket_man.loggers import logger


class Tickets(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.tickets'

    ticket = SlashCommandGroup('ticket', description="Ticket Commands")
    ticket_admin = ticket.create_subgroup('admin', description="Ticket Admin Commands",
                                          default_member_permissions=Permissions(administrator=True))

    @ticket.command(name="create", description="Create a new ticket")
    async def ticket_create(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)
        await ctx.respond(view=TicketSubmitView())

    @ticket.command(name="view", description="View a ticket")
    async def ticket_view(self, ctx: ApplicationContext):
        """View a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond(view=ViewTicketEmbed())

    @ticket.command(name="close", description="Close your open/latest ticket.")
    async def ticket_close(self, ctx: ApplicationContext, ticket_id: int = None):
        await ctx.defer(ephemeral=True)
        view = discord.ui.View()
        view.add_item(TicketCloseButton(ticket_id=ticket_id))
        await ctx.respond()

    @ticket.command(name="comment", description="Add a comment to a ticket.")
    async def ticket_comment(self, ctx: ApplicationContext):
        """Add a comment to an open ticket."""
        await ctx.defer(ephemeral=True)
        await ctx.respond(view=CommentTicketView())

    @ticket.command(name="list", description="List your open tickets.")
    async def ticket_list(self, ctx: ApplicationContext):
        """List your open tickets."""
        await ctx.defer(ephemeral=True)
        # TODO: only list most recent 5 tickets

        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="delete", description="Delete a ticket.")
    @default_permissions(administrator=True)
    async def ticket_delete(self, ctx: ApplicationContext, ticket_id: int):
        """Delete a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        ticket = await get_ticket(ticket_id)
        if ticket.user_id != ctx.author.id:
            await ctx.respond("You cannot delete a ticket that is not yours.")
            return
        else:
            if ticket is None:
                await ctx.respond("Ticket not found.")
                return
            else:
                await ctx.respond(view=TicketDeleteButton(ticket_id))

    @ticket_admin.command(name="list", description="List all open tickets.")
    @default_permissions(administrator=True)
    async def ticket_admin_list(self, ctx: ApplicationContext):
        """List all open tickets."""
        await ctx.defer(ephemeral=True)
        tickets = await get_all_open_tickets()
        if tickets is None:
            await ctx.respond("There are no open tickets.")
            return
        else:
            pages = []
            first_page = discord.Embed(title="Open Tickets", timestamp=arw.now('US/Eastern').datetime, description="All open tickets are listed on the following pages.")
            pages.append(Page(embeds=[first_page]))
            for ticket in tickets:
                pages.append(Page(embeds=[make_embed(ticket)], custom_view=make_view(ticket)))
            pager = Paginator(pages=pages)
            await pager.respond(ctx.interaction, ephemeral=True)

    @ticket_admin.command(name="close", description="Close a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_close(self, ctx: ApplicationContext, ticket_id: int):
        """Close a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        ticket = close_ticket(ticket_id)

    @ticket_admin.command(name="comment", description="Add a comment to a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_comment(self, ctx: ApplicationContext):
        """Add a comment to a ticket."""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="open", description="ReOpen a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_open(self, ctx: ApplicationContext, ticket_id: int):
        """Open a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        ticket = await open_ticket(ticket_id)
        await ctx.respond(f"Ticket {ticket.id} (re)opened.")

    @ticket_admin.command(name="edit", description="Edit a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_edit(self, ctx: ApplicationContext):
        """Edit a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="addtesttickets", description="Add test tickets.")
    @default_permissions(administrator=True)
    async def ticket_admin_addtest(self, ctx: ApplicationContext):
        """Add test tickets."""
        await ctx.defer(ephemeral=True)
        await add_test_tickets()

    @ticket_admin.command(name="view", description="View a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_view(self, ctx: ApplicationContext, ticket_id: int):
        """View a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        ticket = await get_ticket(ticket_id)
        if ticket is None:
            await ctx.respond("Ticket not found.")
            return
        else:
            page = ticket
            paginator = Paginator([])
            paginator.pages.append(Page(embeds=[make_embed(ticket)], custom_view=make_view(ticket, paginator)))

    @ticket_admin.command(name="view_comments", description="View a ticket's comments.")
    @default_permissions(administrator=True)
    async def ticket_admin_view_comments(self, ctx: ApplicationContext):
        """View comments on a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="list_closed", description="List all closed tickets.")
    @default_permissions(administrator=True)
    async def ticket_admin_list_closed(self, ctx: ApplicationContext):
        """List all closed tickets."""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @Cog.listener()
    async def on_ready(self):
        logger.info(f'{self.ext_path} loaded successfully.')


def setup(bot):
    bot.add_cog(Tickets(bot))
    logger.info('Loaded Tickets')


def teardown(bot):
    bot.remove_cog(Tickets(bot))
    logger.info('Unloaded Tickets')
