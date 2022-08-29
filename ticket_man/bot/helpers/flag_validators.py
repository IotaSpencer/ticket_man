from typing import Any, Union

from discord.ext.commands import FlagConverter

from ticket_man.utils import dotdict
from ticket_man.bot.helpers.flag_converters import TodoAddFlags


def validations(argument: Union[str, int, bool, Any], criteria: dict):
    """Validate criteria"""
    for name, constraints in criteria.items():
        print(name, constraints)
        for constraint, value in constraints.items():
            print(constraint, value)
            if constraint == 'is_string':
                if not isinstance(value, str):
                    return False
            elif constraint == 'is_int':
                if not isinstance(value, int):
                    return False
                else:
                    if argument < value.min_value or argument > value.max_value:
                        return False
            elif constraint == 'is_bool':
                if not isinstance(value, bool):
                    return False
        return True


def validate(function: str, flags: FlagConverter):
    """Validate flags"""
    class_, command = function.split('-')
    validators = {
        'todo': {
            'add': {
                'content':   ('constraints', {'is_string': True}),
                'priority':  ('constraints', {'is_int': True, 'min_value': 1, 'max_value': 5}),
                'completed': ('constraints', {'is_bool': True})
            }
        }
    }
    validations(flags, validators[class_][command])
    return True
