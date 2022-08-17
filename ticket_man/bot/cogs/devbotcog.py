# built-in

# 3rd party
from discord.ext.commands import Cog, command
from discord import AutoShardedBot
# local
from ticket_man.loggers import logger
from ticket_man.bot.helpers.discord_helpers import *
import ticket_man.bot.bot


class DevBotCog(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: Union[Bot, AutoShardedBot, discord.ext.bridge.Bot, ticket_man.bot.bot.Bot, ticket_man.bot.bot.DevBot, ticket_man.bot.bot.ProdBot]):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.devbotcog'

    @Cog.listener('on_message')
    async def self_is_dev(self, message: Message):
        """
        Since this only loaded on the DevBot, we don't need to check if it is the dev bot
        """
        if check_if_tester_or_main_bot(message, self.bot):
            pass # If they are a tester, act casual
        else: # We're devbot, and user is not a tester
            if message.author.id != self.bot.user.id:
                if message.author.bot == False:
                    if message.channel.__class__.__name__ == 'DMChannel':
                        await reply_self_is_dev2(message, self.bot)

def setup(bot):
    bot.add_cog(DevBotCog(bot))
    logger.info('Loaded DevBotCog')


def teardown(bot):
    bot.remove_cog(DevBotCog(bot))
    logger.info('Unloaded DevBotCog')
