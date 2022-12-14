# built-in
import datetime
# 3rd party
import arrow as arw
import discord.ui
from discord.cog import Cog
from discord.commands import SlashCommandGroup
from discord import ApplicationContext, Embed, Permissions, default_permissions
from discord.ext.pages import Page, Paginator

from ticket_man.bot.helpers import is_server_owner
from ticket_man.bot.helpers.db_abbrevs import \
    add_test_comments, add_test_tickets, close_ticket, get_all_open_tickets, get_last_5_tickets_by_user, \
    get_latest_ticket, \
    get_ticket, get_user_ticket, open_ticket, delete_ticket, get_ticket_comment, \
    get_ticket_comments, get_all_ticket_comments, get_all_user_tickets, \
    get_all_comments, get_all_tickets, get_all_user_open_tickets
from ticket_man.bot.helpers.db_funcs import get_all_closed_tickets
from ticket_man.bot.helpers.db_funcs.db_bools import has_comments
from ticket_man.bot.helpers.ticket_objects.views.ticket_admin_comment import TicketAdminCommentModal
from ticket_man.bot.helpers.ticket_objects.views.ticket_admin_edit import TicketAdminEditView

# local
from ticket_man.bot.helpers.ticket_objects.views.ticket_comment import CommentTicketView
from ticket_man.bot.helpers.ticket_objects.views.ticket_submit import TicketSubmitView
from ticket_man.bot.helpers.ticket_objects.make_pages import TicketCloseButton, TicketDeleteButton, make_comment_embed, \
    make_embed, \
    make_view
from ticket_man.loggers import logger


class Tickets(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.tickets'

    ticket = SlashCommandGroup('ticket', description="Ticket Commands")
    ticket_admin = SlashCommandGroup('ticket_admin', description="Ticket Admin Commands",
                                     default_member_permissions=Permissions(administrator=True))

    @ticket.command(name="create", description="Create a new ticket")
    async def ticket_create(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)
        tickets = get_all_user_open_tickets(ctx.author.id)
        if len(tickets()) > 0:
            await ctx.respond(f"You already have an open ticket! Please close it before opening a new one.",
                              ephemeral=True)
            return
        await ctx.respond(view=TicketSubmitView())

    @ticket.command(name="view", description="View a ticket")
    async def ticket_view(self, ctx: ApplicationContext, ticket_id: int):
        """View a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        ticket = get_user_ticket(ticket_id, ctx.author.id)
        ticket = ticket[0]
        if ticket is None:
            await ctx.respond(f"Ticket {ticket_id} not found")
            return
        pager = Paginator(pages=[Page(embeds=[await make_embed(ticket, bot=ctx.bot)])])
        await pager.respond(ctx.interaction, ephemeral=True)

    @ticket.command(name="close", description="Close your latest open ticket.")
    async def ticket_close(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)
        ticket = get_latest_ticket(ctx.author.id)
        if ticket is None:
            await ctx.respond(f"You don't have any open tickets!")
            return

        closed = close_ticket(ticket.id)
        if closed:
            await ctx.respond(f"Closed ticket {ticket.id}")

    @ticket.command(name="comment", description="Add a comment to a ticket.")
    async def ticket_comment(self, ctx: ApplicationContext):
        """Add a comment to an open ticket."""
        await ctx.defer(ephemeral=True)
        await ctx.respond(view=CommentTicketView())

    @ticket.command(name="list", description="List your open tickets.")
    async def ticket_list(self, ctx: ApplicationContext):
        """List your open tickets."""
        await ctx.defer(ephemeral=True)
        tickets = get_last_5_tickets_by_user(ctx.author.id)
        pages = []
        for ticket in tickets:
            pages.append(Page(embeds=[await make_embed(ticket, bot=ctx.bot)]))
        paginator = Paginator(pages=pages, timeout=60)
        await paginator.respond(ctx.interaction, ephemeral=True)

    @ticket.command(name="delete", description="Delete a ticket.")
    async def ticket_delete(self, ctx: ApplicationContext, ticket_id: int):
        """Delete a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        ticket = get_ticket(ticket_id)
        if ticket is not None:
            if ticket.user_id != ctx.author.id:
                await ctx.respond("You cannot delete a ticket that is not yours.")
                return
            else:
                deleted = delete_ticket(ticket.id)
                if deleted:
                    await ctx.respond(f"Deleted ticket {ticket.id}")
        else:
            await ctx.respond(f"Ticket {ticket_id} not found")
            return

    @ticket_admin.command(name="list", description="List all open tickets.")
    @default_permissions(administrator=True)
    async def ticket_admin_list(self, ctx: ApplicationContext):
        """List all open tickets."""
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        await ctx.defer(ephemeral=False)
        tickets = get_all_open_tickets()
        if tickets is None:
            await ctx.respond("There are no open tickets.")
            return
        else:
            pages = []
            first_page = discord.Embed(title="Open Tickets", timestamp=arw.now('US/Eastern').datetime,
                                       description="All open tickets are listed on the following pages.")
            pages.append(Page(embeds=[first_page]))
            for ticket in tickets:
                pages.append(Page(embeds=[await make_embed(ticket, bot=ctx.bot)], custom_view=make_view(ticket)))
            pager = Paginator(pages=pages)
            await pager.respond(ctx.interaction, ephemeral=False)

    @ticket_admin.command(name="close", description="Close a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_close(self, ctx: ApplicationContext, ticket_id: int):
        """Close a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        ticket = close_ticket(ticket_id)

    @ticket_admin.command(name="delete", description="Delete a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_delete(self, ctx: ApplicationContext, ticket_id: int):
        """Delete a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        deleted = delete_ticket(ticket_id)
        if deleted:
            await ctx.respond(f"Deleted ticket {ticket_id}")

    @ticket_admin.command(name="comment", description="Add a comment to a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_comment(self, ctx: ApplicationContext, ticket_id: int):
        """Add a comment to a ticket."""
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        await ctx.send_modal(TicketAdminCommentModal(title=f"Adding comment to {ticket_id}.",
                                                     extra_kwargs={'ticket_id': ticket_id, 'bot': ctx.bot}))

    @ticket_admin.command(name="open", description="ReOpen a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_open(self, ctx: ApplicationContext, ticket_id: int):
        """Open a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        ticket = open_ticket(ticket_id)
        await ctx.respond(f"Ticket {ticket.id} (re)opened.")

    @ticket_admin.command(name="edit", description="Edit a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_edit(self, ctx: ApplicationContext, ticket_id: int):
        """Edit a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        ticket = get_ticket(ticket_id)
        if ticket is None:
            await ctx.respond(f"Ticket {ticket_id} not found.")
            return
        await ctx.respond(
            f"Please note, command must be used once per field.  If you want to edit multiple fields, you must "
            f"run the command multiple times.", ephemeral=True, delete_after=20)
        await ctx.respond(f"Editing ticket {ticket_id}.",
                          view=TicketAdminEditView(extra_kwargs={"ticket_id": ticket_id}), ephemeral=True)

    @ticket_admin.command(name="addtesttickets", description="Add test tickets.")
    @default_permissions(administrator=True)
    async def ticket_admin_addtest(self, ctx: ApplicationContext):
        """Add test tickets."""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        await add_test_tickets()

    @ticket_admin.command(name="addtestcomments", description="Add test comments.")
    @default_permissions(administrator=True)
    async def ticket_admin_addtestcomments(self, ctx: ApplicationContext):
        """Add test comments."""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        add_test_comments()
        await ctx.respond("Added test comments.")

    @ticket_admin.command(name="view", description="View a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_view(self, ctx: ApplicationContext, ticket_id: int):
        """View a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        ticket = get_ticket(ticket_id)
        if ticket is None:
            await ctx.respond("Ticket not found.")
            return
        else:
            paginator = Paginator(
                    pages=[Page(embeds=[await make_embed(ticket, bot=ctx.bot)], custom_view=make_view(ticket))])
            await paginator.respond(ctx.interaction, ephemeral=False)

    @ticket_admin.command(name="view_comments", description="View a ticket's comments.")
    @default_permissions(administrator=True)
    async def ticket_admin_view_comments(self, ctx: ApplicationContext, ticket_id: int):
        """View comments on a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        ticket = get_ticket(ticket_id)
        if ticket is None:
            await ctx.respond("Ticket not found.")
            return
        else:
            comments = get_ticket_comments(ticket_id)
            if comments() is None:
                await ctx.respond("No comments found.")
                return
            else:
                pages = []
                first_page = discord.Embed(title=f"Comments for Ticket {ticket_id}",
                                           timestamp=arw.now('US/Eastern').datetime,
                                           description="All comments are listed on the following pages.")
                pages.append(Page(embeds=[first_page]))
                for comment in comments().scalars().all():
                    pages.append(Page(embeds=[await make_comment_embed(comment, bot=ctx.bot)]))
                pager = Paginator(pages=pages)
                await pager.respond(ctx.interaction, ephemeral=True)

    @ticket_admin.command(name="list_closed", description="List all closed tickets.")
    @default_permissions(administrator=True)
    async def ticket_admin_list_closed(self, ctx: ApplicationContext):
        """List all closed tickets."""
        await ctx.defer(ephemeral=True)
        if not await is_server_owner(ctx):
            await ctx.respond("You must be the server owner to use this command.")
            return
        tickets = get_all_closed_tickets()
        if tickets is None:
            await ctx.respond("No closed tickets found.")
            return
        else:
            pages = []
            first_page = discord.Embed(title="Closed Tickets", timestamp=arw.now('US/Eastern').datetime,
                                       description="All closed tickets are listed on the following pages.")
            pages.append(Page(embeds=[first_page]))
            for ticket in tickets:
                pages.append(Page(embeds=[await make_embed(ticket, bot=ctx.bot)]))
            pager = Paginator(pages=pages)
            await pager.respond(ctx.interaction, ephemeral=True)


def setup(bot):
    bot.add_cog(Tickets(bot))
    logger.info('Loaded Tickets')


def teardown(bot):
    bot.remove_cog(Tickets(bot))
    logger.info('Unloaded Tickets')
