# built-in
# 3rd party
import discord.ui
from discord.cog import Cog
from discord.commands import SlashCommandGroup
from discord import ApplicationContext, Embed, Permissions, default_permissions

from ticket_man.bot.helpers.db_abbrevs import add_test_tickets, get_ticket
from ticket_man.bot.helpers.ticket_objects.ticket_view_buttons import TicketCloseButton, TicketDeleteButton, \
    TicketOpenButton
# local
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_close import CloseTicketEmbed
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_comment import CommentTicketView
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_submit import TicketSubmitView
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_view import ViewTicketEmbed
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
    async def ticket_close(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)
        await ctx.respond(view=CloseTicketEmbed())

    @ticket.command(name="comment", description="Add a comment to a ticket.")
    async def ticket_comment(self, ctx: ApplicationContext):
        """Add a comment to an open ticket."""
        await ctx.defer(ephemeral=True)
        await ctx.respond(view=CommentTicketView())

    @ticket.command(name="list", description="List your open tickets.")
    async def ticket_list(self, ctx: ApplicationContext):
        """List your open tickets."""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="delete", description="Delete a ticket.")
    @default_permissions(administrator=True)
    async def ticket_delete(self, ctx: ApplicationContext):
        """Delete a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="list", description="List all open tickets.")
    @default_permissions(administrator=True)
    async def ticket_admin_list(self, ctx: ApplicationContext):
        """List all open tickets."""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="close", description="Close a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_close(self, ctx: ApplicationContext):
        """Close a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="comment", description="Add a comment to a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_comment(self, ctx: ApplicationContext):
        """Add a comment to a ticket."""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="open", description="ReOpen a ticket.")
    @default_permissions(administrator=True)
    async def ticket_admin_open(self, ctx: ApplicationContext):
        """Open a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

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
        embed = Embed(title=f"Ticket #{ticket_id}")
        embed.add_field(name='Ticket Status', value=ticket.open)
        embed.add_field(name='Ticket Type', value=ticket.type)
        embed.add_field(name='Ticket Creator', value=ticket.user_id)
        # embed.add_field(name='Ticket Comments', value=ticket.comments)
        view = discord.ui.View()

        view.add_item(TicketDeleteButton(ticket_id=ticket_id))
        view.add_item(TicketCloseButton(ticket_id=ticket_id))
        view.add_item(TicketOpenButton(ticket_id=ticket_id))
        await ctx.respond(embed=embed, view=view)


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
