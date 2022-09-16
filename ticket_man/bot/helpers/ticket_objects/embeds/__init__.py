import discord
from .ticket_admin_view import AdminViewTicketEmbed
from .ticket_close import CloseTicketEmbed
from .ticket_comment import CommentTicketView, TicketCommentModal
from .ticket_submit import TicketSubmitView
from .ticket_list import ListTicketEmbed
from .ticket_view import ViewTicketEmbed


class EmbedBase(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subject = kwargs.pop("subject", None)
        body = kwargs.pop("body", None)
        status = kwargs.pop("status", None)
        type_ = kwargs.pop("type_", None)
        user = kwargs.pop("user", None)
        self.add_field(name="Subject", value=f"{subject}")
        self.add_field(name="Body", value=f"{body}")
        self.add_field(name="Status", value=f"{status}")
        self.add_field(name="Type", value=f"{type_}")
        self.add_field(name="User", value=f"{user}")