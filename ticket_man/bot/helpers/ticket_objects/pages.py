import asyncio

import discord
from discord.ext import pages
from discord.ext.pages import PaginatorButton
from discord.ui import View

from ticket_man.bot.helpers.db_abbrevs import get_all_tickets, get_ticket
from ticket_man.bot.helpers.ticket_objects.ticket_view_buttons import TicketCloseButton, TicketDeleteButton, \
    TicketOpenButton



class TicketPage:
    def __init__(self, ticket, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ticket = ticket
        self.ticket_id = kwargs.pop('ticket_id', None)
        self.ticket_id = ticket.id
        self.embeds = [self.make_embed()]
        self.custom_view = self.make_view()

    def get_ticket(self):
        return self.ticket

    def make_embed(self):
        ticket = self.ticket
        embed = discord.Embed(title=f"Ticket {ticket.id}", color=0x00ff00)
        embed.add_field(name="Ticket ID", value=f"{ticket.id}", inline=False)
        embed.add_field(name="Ticket Status (open-1/closed-0)", value=f"{ticket.open}", inline=False)
        embed.add_field(name="Ticket Author", value=f"{ticket.user_id}", inline=False)
        embed.add_field(name="Ticket Subject", value=f"{ticket.subject}", inline=False)
        embed.add_field(name="Ticket Content", value=f"{ticket.content}", inline=False)
        embed.add_field(name="Ticket Created", value=f"{ticket.created}", inline=False)
        embed.add_field(name="Ticket Last Updated", value=f"{ticket.last_updated}", inline=False)
        embed.add_field(name="Ticket Last Updated By", value=f"{ticket.last_updated_by}", inline=False)

        return embed

    def make_view(self):
        ticket = self.ticket
        view = discord.ui.View()
        view.add_item(TicketCloseButton(ticket_id=ticket.id))
        view.add_item(TicketDeleteButton(ticket_id=ticket.id))
        view.add_item(TicketOpenButton(ticket_id=ticket.id))
        return view


class TicketPager(object):
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.pages = kwargs.pop('pages', [])
        tickets = kwargs.pop('tickets', None)

        for ticket in tickets:
            self.pages.append(TicketPage(ticket=ticket))

    def paginator(self, page_list=None, **kwargs):
        paginator_class = pages.Paginator(pages=[])
        pages_ = kwargs.pop('pages', page_list)  # type: list[pages.PageGroup] | list[pages.Page] | list[str] | list[list[discord.Embed] | discord.Embed]
        show_disabled: bool = kwargs.pop('show_disabled') or True
        show_indicator: bool = kwargs.pop('show_indicator') or True
        show_menu: bool = kwargs.pop('show_menu') or False
        menu_placeholder: str = "Select Page Group"
        author_check: bool = kwargs.pop('author_check') or True
        disable_on_timeout: bool = kwargs.pop('disable_on_timeout') or True
        use_default_buttons: bool = kwargs.pop('use_default_buttons') or True
        default_button_row: int = kwargs.pop('default_button_row') or 0
        loop_pages: bool = kwargs.pop('loop_pages') or False
        custom_view: View | None = kwargs.pop('custom_view') or None
        timeout: float | None = kwargs.pop('timeout') or 180.0
        custom_buttons: list[PaginatorButton] | None = kwargs.pop('custom_buttons') or None
        trigger_on_display: bool | None = kwargs.pop('trigger_on_display') or None
        if use_default_buttons:
            paginator_class.add_button(PaginatorButton(emoji='⏮', style=discord.ButtonStyle.green, row=default_button_row,
                                                       button_type='first'))
            paginator_class.add_button(PaginatorButton(emoji='◀', style=discord.ButtonStyle.green, row=default_button_row,
                                                       button_type='back'))
            paginator_class.add_button(PaginatorButton(button_type='page_indicator', style=discord.ButtonStyle.green, row=default_button_row))
            paginator_class.add_button(PaginatorButton(emoji='▶', style=discord.ButtonStyle.green, row=default_button_row,
                                                       button_type='next'))
            paginator_class.add_button(PaginatorButton(emoji='⏭', style=discord.ButtonStyle.green, row=default_button_row,
                                                       button_type='last'))
        paginator_class.pages = pages_ or self.pages
        paginator_class.show_disabled = show_disabled
        paginator_class.show_indicator = show_indicator
        paginator_class.show_menu = show_menu
        paginator_class.menu_placeholder = menu_placeholder
        paginator_class.author_check = author_check
        paginator_class.disable_on_timeout = disable_on_timeout
        paginator_class.use_default_buttons = use_default_buttons
        paginator_class.default_button_row = default_button_row
        paginator_class.loop_pages = loop_pages
        paginator_class.custom_view = custom_view
        paginator_class.timeout = timeout
        paginator_class.custom_buttons = custom_buttons
        paginator_class.trigger_on_display = trigger_on_display
        return paginator_class

    @staticmethod
    def make_page(*args, **kwargs):
        return TicketPage(*args, **kwargs)

    def get_page(self, page_number):
        return self.pages[page_number]

    def get_page_count(self):
        return len(self.pages)

    def add_page(self, page):
        self.pages.append(page)

    def remove_page(self, page):
        self.pages.remove(page)

    def clear_pages(self):  # clears all pages
        self.pages.clear()

    def pop_page(self, index):  # pops a page at a given index
        self.pages.pop(index)

    def insert_page(self, index, page):  # inserts a page at a given index
        self.pages.insert(index, page)

    def extend_pages(self, pages):  # extends the pages with a list of pages
        self.pages.extend(pages)

    def index(self, page):  # returns the index of a page
        return self.pages.index(page)

    def count(self, page):  # returns the number of times a page appears
        return self.pages.count(page)

    def __repr__(self):
        return f"<{self.__class__.__name__} pages={self.pages}>"

    def __str__(self):
        return self.pages

    def __len__(self):
        return len(self.pages)

    def __iter__(self):
        return iter(self.pages)

    def __getitem__(self, index):
        return self.pages[index]

    def __setitem__(self, index, value):
        self.pages[index] = value

    def __delitem__(self, index):
        self.pages.pop(index)

    def __del__(self):
        del self.pages

    def __contains__(self, item):
        return item in self.pages

    def __add__(self, other):
        return self.pages + other

    def __iadd__(self, other):
        self.pages += other
        return self.pages

    def __sub__(self, other):
        return self.pages.remove(other)

    def __isub__(self, other):
        self.pages -= other
        return self.pages
