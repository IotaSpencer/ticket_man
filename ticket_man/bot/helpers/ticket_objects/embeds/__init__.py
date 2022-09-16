import importlib
base = 'ticket_man.bot.helpers.ticket_objects.embeds.'
for path in ['admin_view', 'close', 'comment', 'submit', 'view', 'admin_list', 'admin_close', 'admin_comment', 'admin_open', 'admin_edit']:
    print(f"import ticket_{path}")
    importlib.import_module(f'{base}ticket_{path}')


