# Docs: https://docs.pycord.dev/en/master/ext/pages/index.html

# This example demonstrates a standalone cog file with the bot instance in a separate file.

# Note that the below examples use a Slash Command Group in a cog for
# better organization and doing so is not required for using ext.pages.

import asyncio

import discord
from discord.ext import pages


class BasePage(pages.Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class TicketPager(object):
    def __init__(self, bot):
        self.bot = bot
        self.pages = [

        ]

    @staticmethod
    def make_page(*args, **kwargs):
        return BasePage(*args, **kwargs)

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
        return self.pages - other

    def __isub__(self, other):

        self.pages -= other
        return self.pages


