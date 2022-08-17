import logging
from logging import LogRecord
from ticket_man.logger.helpers import escape

class EscapeFilenameforDiscord(logging.Filter):
    def filter(self, record):
        if record.filename:
            record.filename = escape(record.filename)
            record.funcName = escape(record.funcName)
        return True

class LevelFilter(logging.Filter):
    """
    This is a filter which changes the levelname to that of its Initial letter

    """

    def filter(self, record):
        record.level_initial = record.levelname[0]
        return True

class EmojiFilter(logging.Filter):
    """This is a filter that replaces levelname with emojis"""

    def filter(self, record: LogRecord) -> bool:
        level = record.levelname
        levels = {
            'WARNING': '⚠',
            'ERROR': '‼',
            'CRITICAL': '☠',
            'DEBUG': '❓',
            'INFO': '✅'
        }
        try:
            record.level_emoji = levels[level]
            return True
        except:
            return False


emoji_filter = EmojiFilter()
level_filter = LevelFilter()
markdown_filter = EscapeFilenameforDiscord()
