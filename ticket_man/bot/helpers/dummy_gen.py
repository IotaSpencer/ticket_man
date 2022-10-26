import aiohttp

from ticket_man.utils import dotdict


def user_data():
    users = []
    admin = []
    # add ticket ids into dict
    users.append(dotdict({
        "tag": "morgs#0920",
        "id": 201063045491851264,
        "ticket_id": 1,
        "admin": False,
        "name": "crypto1324"
    }))
    admin.append(dotdict({
        "tag": "IotaSpencer#0001",
        "id": 234093061045616642,
        "admin": True,
        "name": "iotaspencer"
    }))
    users.append(dotdict({
        "tag": "GameWizard13#8485",
        "name": "neko(mtf)",
        "id": 316002085369937920,
        "ticket_id": 15,
        "admin": False
    }))
    users.append(dotdict({
        "tag": "UNICORPSE#5899",
        "name": "axel 🦊",
        "id": 364190414254637069,
        "admin": False
    }))
    users.append(dotdict({
        "tag": "Hermän2000#9583",
        "name": "Hermän2000",
        "id": 326738183184318464,
        "ticket_id": 5,
        "admin": False
    }))
    users.append(dotdict({
        "tag": "IotaTest#9473",
        "name": "IotaTest",
        "id": 934701743743324180,
        "ticket_id": 203,
        "admin": False
    }))
    return users, admin

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
