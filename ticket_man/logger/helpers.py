import re


def escape(str: str) -> str:
    # \ -> \\
    str = str.replace("""\\""", """\\\\""")
    # - -> \_
    str = str.replace("_", "\\_")
    # * -> \*
    str = str.replace("""*""", "\\*")
    # ~ -> \~
    str = str.replace("~", "\\~")
    # ` -> \`
    str = str.replace("`", "\\`")
    # | -> \|
    str = str.replace('|', "\\|")

    return str
