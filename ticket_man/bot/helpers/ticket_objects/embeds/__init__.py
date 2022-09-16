import importlib
base = 'ticket_man.bot.helpers.ticket_objects.embeds.'
for path in ['admin_view', 'close', 'comment', 'submit', 'view', 'admin_list', 'admin_close', 'admin_comment', 'admin_open', 'admin_edit']:
    print(f"import ticket_{path}")
    importlib.import_module(f'{base}ticket_{path}')


class EmbedBase(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subject = kwargs.pop("subject", None)
        body = kwargs.pop("body", None)
        status = kwargs.pop("status", None)
        type_ = kwargs.pop("type_", None)
        user = kwargs.pop("user", None)
        self.add_field(name="Subject", value=f"{subject}")
        self.add_field(name="Body", value=f"{body}")
        self.add_field(name="Status", value=f"{status}")
        self.add_field(name="Type", value=f"{type_}")
        self.add_field(name="User", value=f"{user}")