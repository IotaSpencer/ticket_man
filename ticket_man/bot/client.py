# built-ins(?)

# (3rd party)
import discord

# local import
from ticket_man.bot.bot import DevBot, ProdBot
from ticket_man.config import Configs


async def start(env) -> None:
    """

    :rtype: object
    """
    token = ''

    bot = {}
    print(env)
    if env == 'prod':
        bot = ProdBot(intents=discord.Intents.all())
        token = Configs.cfg.bot.token
        bot.disable_sending = False

    elif env == 'dev':
        bot = DevBot(intents=discord.Intents.all())
        token = Configs.dcfg.bot.token
        bot.disable_sending = True
        bot.load_extension('jishaku')
        bot.load_extension('ticket_man.bot.cogs.devbotcog')

    # Load Jishaku
    bot.load_extension('ticket_man.bot.cogs.extensions')
    bot.load_extension('ticket_man.bot.cogs.admin')
    bot.load_extension('ticket_man.bot.cogs.confirm')
    bot.load_extension('ticket_man.bot.cogs.fun')
    bot.load_extension('ticket_man.bot.cogs.owner')
    bot.load_extension('ticket_man.bot.cogs.id_stuff')
    bot.load_extension('ticket_man.bot.cogs.hello')
    bot.load_extension('ticket_man.bot.cogs.join_message')
    bot.load_extension('ticket_man.bot.cogs.age_calc')
    bot.load_extension('ticket_man.bot.cogs.purge_users')

    await bot.start(token)
