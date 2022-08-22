# built-ins(?)

# (3rd party)
import discord

# local import
from ticket_man.bot.bot import Bot
from ticket_man.config import Configs


async def start(env: str) -> None:
    """
    :type env: str
    :rtype: object
    """
    token = ''

    bot = {}
    print(env)
    if env == 'prod':
        bot = Bot(intents=discord.Intents.all())
        token = Configs.cfg.bot.token
        bot.disable_sending = False

    elif env == 'dev':
        bot = Bot(intents=discord.Intents.all())
        token = Configs.cfg.bot.token
        # bot.disable_sending = True
        bot.load_extension('jishaku')
        bot.load_extension('ticket_man.bot.cogs.devbotcog')

    # Load Jishaku
    bot.load_extension('ticket_man.bot.cogs.admin')
    bot.load_extension('ticket_man.bot.cogs.extensions')
    bot.load_extension('ticket_man.bot.cogs.todo')
    bot.load_extension('ticket_man.bot.cogs.join_message')
    bot.load_extension('ticket_man.bot.cogs.owner')

    await bot.start(token)
