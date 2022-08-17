# built-in
# 3rd party
import discord
import omegaconf.errors
from discord.ext import bridge
import arrow as arw
# local
from ticket_man.config import Configs
from ticket_man.loggers import logger
from ticket_man.bot.helpers.discord_helpers import *
from ticket_man.bot.helpers.decorators import *


class Bot(bridge.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        db_guilds = Configs.sdb.servers.keys()
        debug_guilds = [server for server in db_guilds]
        self.debug_guilds = debug_guilds
        self.max_messages = 10000
        self.status = discord.Status.online
    async def on_ready(self):
        logger.info(f"Bot is online and ready! Name is {self.user}")
        app = await self.application_info()
        app_name = app.name
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f"{app_name}"
        ), status=discord.Status.online)

class DevBot(Bot):
    def __init__(self, **options):
        super().__init__(**options)
        prefix = Configs.dcfg.bot.prefix
        self.command_prefix = prefix
        try:
            self.owner_ids = Configs.dcfg.bot.owners
            # puts(self.owner_ids)
        except omegaconf.errors.ConfigAttributeError:
            self.owner_ids = [Configs.dcfg.bot.owner]

class ProdBot(Bot):
    def __init__(self, **options):
        super().__init__(**options)
        prefix = Configs.cfg.bot.prefix
        self.command_prefix = prefix
        try:
            self.owner_ids = Configs.cfg.bot.owners
            # puts(self.owner_ids)
        except omegaconf.errors.ConfigAttributeError:
            self.owner_ids = [Configs.cfg.bot.owner]
