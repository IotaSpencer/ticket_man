from collections import namedtuple
from dataclasses import dataclass
from typing import TypedDict

import aiohttp
import asyncio
@dataclass
class Users:
    tag: str
    id: int
    admin: bool

    users = []

    def __init__(self, tag, id, admin):
        self.tag = tag
        self.id = id
        self.admin = admin

    def add_user(self, user):
        self.tag = user.tag
        self.id = user.id
        self.admin = user.admin
Users.add_user

        "tag": "IotaSpencer#0001",
        "id": 234093061045616642
    },
    {morgs  # 0920 (crypto1324)  - 201063045491851264}
    GameWizard(neko(mtf)) - 316002085369937920
    UNICORPSE  # 5899 (axel 🦊) - 364190414254637069

class DummyGen:

    def __init__(self, **kwargs):
        # (integer) - The number of paragraphs to generate.
        # short, medium, long, verylong - The average length of a paragraph.
        # decorate - Add bold, italic and marked text.
        # link - Add links.
        # ul - Add unordered lists.
        # ol - Add numbered lists.
        # dl - Add description lists.
        # bq - Add blockquotes.
        # code - Add code samples.
        # headers - Add headers(headings).
        # allcaps - Use ALL CAPS.
        # prude - Prude version.
        # plaintext - Return plain text, no HTML.
        self.session = None
        self.para = kwargs.pop('para', 1)
        self.para_len = kwargs.pop('para_len', 'short')
        self.plain = kwargs.pop('plain', 'plaintext')

    async def init_session(self):
        self.session = aiohttp.ClientSession("https://loripsum.net")

    async def get_response(self, para=None, para_len=None, plain=None):
        if not self.session:
            await self.init_session()
        if para is None:
            para = self.para
        if para_len is None:
            para_len = self.para_len
        if plain is None:
            plain = ''
        else:
            plain = 'plaintext'
        async with self.session.get(f"/api/{para}/{para_len}/{plain}") as resp:
            return await resp.text()
