import sys
from tabulate import tabulate
from note.helpers import type_check, format_for_tabulate

class DisplayModule(object):
    """
    Display Module
    """
    SHELL_FILTERS = ['vision', 'thought', 'tag_name', 'created']
    TAG_FILTERS = ['tag_name']
    SHELL_TAG_FILTERS = ['shell_id', 'tag_id']

    @staticmethod
    def display_options(options=None):
        options = options if options and isinstance(options, dict) else {}

        sys.stdout.write(f'\n{"="*50}\nHow may I help you?\n')

        for key, value in options.items():
            sys.stdout.write(f' {key}: {value}\n')

        sys.stdout.flush()

    @staticmethod
    def display_text(text=''):
        sys.stdout.write(text)
        sys.stdout.flush()

    @staticmethod
    def display_obj_as_table(obj, filters, include_keys=None, exclude_keys=None):
        obj = type_check(obj, (list, tuple), default=())
        # 'filters' needs to be mutable
        filters = list(type_check(filters, (list, tuple), default=()))
        include_keys = type_check(include_keys, (list, tuple), default=())
        exclude_keys = type_check(exclude_keys, (list, tuple), default=())

        filters = list(
            filter(
                lambda x: x not in exclude_keys,
                filters
        ))
        filters = filters + list(include_keys)

        table = format_for_tabulate(obj, filters)

        sys.stdout.write(
            tabulate(
                table,
                headers=[header.capitalize() for header in filters],
                showindex=range(1, len(obj)+1),
                stralign='center',
                numalign='center',
                tablefmt='fancy_grid'
            ))
        sys.stdout.write('\n\n')

        sys.stdout.flush()

    @classmethod
    def display_notes(cls, notes=None, include_id=False):
        include_keys = ['shell_id'] if include_id else None
        exclude_keys = ['thought'] if include_id else None

        cls.display_obj_as_table(notes, cls.SHELL_FILTERS, include_keys=include_keys, exclude_keys=exclude_keys)

    @classmethod
    def display_tags(cls, tags=None):
        cls.display_obj_as_table(tags, cls.TAG_FILTERS)

    @classmethod
    def display_shell_tags(cls, shell_tags=None):
        cls.display_obj_as_table(shell_tags, cls.SHELL_TAG_FILTERS)
