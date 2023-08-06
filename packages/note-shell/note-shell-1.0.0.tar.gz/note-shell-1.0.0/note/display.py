import sys
from tabulate import tabulate

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

    @classmethod
    def convert_shells_to_table_format(cls, notes, filters):
        table = [
            list(
                map(
                    lambda kv: kv[1] if len(kv[1]) < 51 else ''.join([kv[1][:47], '...']),
                    filter(
                        lambda kv: kv[0] in filters,
                        [kv for kv in note.items()]
                ))) for note in notes
        ]

        return table

    @classmethod
    def display_notes(cls, notes=None, include_id=False):
        notes = notes if notes and isinstance(notes, list) else []

        filters = ['shell_id'] + cls.SHELL_FILTERS if include_id else cls.SHELL_FILTERS
        if include_id:
            filters.remove('thought')

        table = cls.convert_shells_to_table_format(notes, filters)

        sys.stdout.write(
            tabulate(
                table,
                headers=[header.capitalize() for header in filters],
                showindex=range(1, len(notes)+1),
                stralign='center',
                numalign='center',
                tablefmt='fancy_grid'
            ))
        sys.stdout.write('\n\n')

        sys.stdout.flush()

    @classmethod
    def convert_tags_to_table_format(cls, tags):
        table = [
            list(
                map(
                    lambda kv: kv[1] if len(kv[1]) < 51 else ''.join([kv[1][:47], '...']),
                    filter(
                        lambda kv: kv[0] in cls.TAG_FILTERS,
                        [kv for kv in tag.items()]
                ))) for tag in tags
        ]

        return table

    @classmethod
    def display_tags(cls, tags=None):
        tags = tags if tags and isinstance(tags, list) else []

        table = cls.convert_tags_to_table_format(tags)

        sys.stdout.write(
            tabulate(
                table,
                headers=[header.capitalize() for header in cls.TAG_FILTERS],
                showindex=range(1, len(tags)+1),
                stralign='center',
                numalign='center',
                tablefmt='fancy_grid'
            ))
        sys.stdout.write('\n\n')

        sys.stdout.flush()

    @classmethod
    def convert_shell_tags_to_table_format(cls, tags):
        table = [
            list(
                map(
                    lambda kv: kv[1] if len(kv[1]) < 51 else ''.join([kv[1][:47], '...']),
                    filter(
                        lambda kv: kv[0] in cls.SHELL_TAG_FILTERS,
                        [kv for kv in tag.items()]
                ))) for tag in tags
        ]

        return table

    @classmethod
    def display_shell_tags(cls, shell_tags=None):
        shell_tags = shell_tags if shell_tags and isinstance(shell_tags, list) else []

        table = cls.convert_shell_tags_to_table_format(shell_tags)

        sys.stdout.write(
            tabulate(
                table,
                headers=[header.capitalize() for header in cls.SHELL_TAG_FILTERS],
                showindex=range(1, len(shell_tags)+1),
                stralign='center',
                numalign='center',
                tablefmt='fancy_grid'
            ))
        sys.stdout.write('\n\n')

        sys.stdout.flush()
