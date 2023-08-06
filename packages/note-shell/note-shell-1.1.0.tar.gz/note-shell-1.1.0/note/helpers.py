from os import system, name
from functools import reduce
from collections import OrderedDict

def clear_screen():
    """
    Clear terminal
    """
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def type_check(element, target_types: list or tuple, default=None):
    """
    Unbound Function to match an object to desired types, and return a default if unmatched
    """
    def object_isinstance(obj, types: list or tuple):
        """ Check if object belongs to a list of types """
        return reduce(
            lambda x, y: x or y,
            [isinstance(obj, type_) for type_ in types]
        )

    target_types = target_types if object_isinstance(target_types, (list, tuple)) else [target_types]

    return element if object_isinstance(element, target_types) else default

def order_obj_for_tabulate(table, order):
    """
    Prepare object in ordered format of keys for tabulate library
    """
    ordered_table = []

    for row in table:
        ordered_row = OrderedDict()

        for key in order:
            if key in row:
                ordered_row[key] = row[key]

        ordered_table.append(ordered_row)

    return ordered_table


def format_for_tabulate(table_obj, filters):
    """
    Format an object for tabulate library, selecting 'filters' as keys from the object
    """
    table_obj = type_check(table_obj, (list, tuple), default=())

    table_obj = order_obj_for_tabulate(table_obj, filters)

    return [
        list(
            map(
                lambda kv: kv[1] if len(kv[1]) < 51 else ''.join([kv[1][:47], '...']),
                filter(
                    lambda kv: kv[0] in filters,
                    [kv for kv in row.items()]
            ))) for row in table_obj
    ]
