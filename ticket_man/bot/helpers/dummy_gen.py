import aiohttp
import asyncio


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
        self.plain = kwargs.pop('plaintext', True)

    async def init_session(self):
        self.session = aiohttp.ClientSession()

    async def get_response(self, para=None, para_len=None, plain=None):
        if not self.session:
            await self.init_session()
        if para is None:
            para = self.para
        if para_len is None:
            para_len = self.para_len
        if plain is None:
            plain = self.plain
        async with self.session.get(f"/api/{para}/{para_len}/{plain}") as resp:
            return await resp.text()
