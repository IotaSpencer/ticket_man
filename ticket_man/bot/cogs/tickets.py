# built-in
# 3rd party
from discord.ext.commands import Cog
from discord.commands import SlashCommandGroup

from discord import ApplicationContext, Permissions, default_permissions

from ticket_man.bot.helpers.ticket_objects.embeds.ticket_close import CloseTicketEmbed
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_comment import CommentTicketView
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_submit import TicketSubmitView
from ticket_man.bot.helpers.ticket_objects.embeds.ticket_view import ViewTicketEmbed
# local
from ticket_man.loggers import logger


class Tickets(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.tickets'

    ticket = SlashCommandGroup('ticket', description="Ticket Commands")
    ticket_admin = ticket.create_subgroup('admin', description="Ticket Admin Commands",
                                          default_member_permissions=Permissions.administrator)

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

    @ticket_admin.command(name="delete")
    @default_permissions(administrator=True)
    async def ticket_delete(self, ctx: ApplicationContext):
        """Delete a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="list")
    @default_permissions(administrator=True)
    async def ticket_admin_list(self, ctx: ApplicationContext):
        """List all open tickets."""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="close")
    @default_permissions(administrator=True)
    async def ticket_admin_close(self, ctx: ApplicationContext):
        """Close a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="comment")
    @default_permissions(administrator=True)
    async def ticket_admin_comment(self, ctx: ApplicationContext):
        """Add a comment to a ticket."""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="open")
    @default_permissions(administrator=True)
    async def ticket_admin_open(self, ctx: ApplicationContext):
        """Open a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="edit")
    @default_permissions(administrator=True)
    async def ticket_admin_edit(self, ctx: ApplicationContext):
        """Edit a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="view")
    @default_permissions(administrator=True)
    async def ticket_admin_view(self, ctx: ApplicationContext):
        """View a ticket (open or closed)"""
        # TODO: One ticket per page, with a paginator
        # TODO: Add a button to delete, close, comment, or edit a ticket
        await ctx.defer(ephemeral=True)

    @ticket_admin.command(name="view-comments")
    @default_permissions(administrator=True)
    async def ticket_admin_view_comments(self, ctx: ApplicationContext):
        """View comments on a ticket (open or closed)"""
        await ctx.defer(ephemeral=True)
        await ctx.respond("This command is not yet implemented.")

    @ticket_admin.command(name="list-closed")
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
