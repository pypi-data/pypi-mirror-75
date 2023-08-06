from note.handler import handle
from note.display import DisplayModule as display

class Cli(object):
    """
    Cli Module
    """
    HELP_OPTIONS = {
        'Interactive': '-i --interactive',
        'Make a quick note': '-s -sm --short-message',
        'Make a normal note': '-n --note',
        'List all notes': '-l -ln --list-notes',
        'List quick notes': '-lq --list-quick-notes',
        'View note': '-v -vn --view-note',
        'List tags': '-lt --list-tags',
        'List notes with tag': '-lnt --list-notes-tag',
    }
    CLI_OPTIONS = {
        '-s': 'quicknote',
        '-sm': 'quicknote',
        '--short-message': 'quicknote',
        '-n': 'normalnote',
        '--note': 'normalnote',
        '-l': 'listnotes',
        '-ln': 'listnotes',
        '--list-notes': 'listnotes',
        '-lq': 'listquicknotes',
        '-list-quick-notes': 'listquicknotes',
        '-v': 'viewnote',
        '-vn': 'viewnote',
        '-view-note': 'viewnote',
        '-lt': 'listtags',
        '--list-tags': 'listtags',
        '-lnt': 'listnotesfortag',
        '--list-notes-tag': 'listnotesfortag',
        '-i': 'pass',
        '--interactive': 'pass',
        '-h': 'help',
        '--help': 'help',
    }
    OPTIONLESS_ARGV_VAL = 'quicknote'
    DEFAULT_CLI = 'pass'
    QUICKNOTE_TAG = '@quicknotes'

    @classmethod
    def evaluate(cls, argv):
        option, value = cls.parse_argv(argv)
        return getattr(cls, 'cli_' + str(option), cls.DEFAULT_CLI)(value)

    @classmethod
    def parse_argv(cls, argv):
        argv = argv if isinstance(argv, list) or isinstance(argv, tuple) else ()

        method_ext = cls.DEFAULT_CLI
        value = None

        if len(argv) > 1 and argv[0] in cls.CLI_OPTIONS:
            method_ext = cls.CLI_OPTIONS[argv[0]]
            value = ' '.join(argv[1:])
        elif len(argv) > 0 and argv[0] in cls.CLI_OPTIONS:
            method_ext = cls.CLI_OPTIONS[argv[0]]
        elif len(argv) > 0 and '-' not in argv[0]:
            method_ext = cls.OPTIONLESS_ARGV_VAL
            value = ' '.join(argv)

        return method_ext, value

    @classmethod
    def cli_quicknote(cls, msg, *args):
        # Return true to continue
        if not msg:
            return True

        handle.handle_option_1(title=msg, description=' ', tag_name=cls.QUICKNOTE_TAG)
        return False

    @classmethod
    def cli_normalnote(cls, *args):
        # Return true to continue
        handle.handle_option_1()
        return False

    @staticmethod
    def cli_listnotes(*args):
        # Return true to continue
        handle.handle_option_2()
        return False

    @staticmethod
    def cli_listnotesfortag(name, *args):
        # Return true to continue
        handle.handle_option_7(name)
        return False

    @classmethod
    def cli_listquicknotes(cls, *args):
        # Return true to continue
        cls.cli_listnotesfortag(cls.QUICKNOTE_TAG)
        return False

    @staticmethod
    def cli_viewnote(index):
        handle.handle_option_4(index)
        return False

    @classmethod
    def cli_help(cls, *args):
        display.display_text('note <option> <input>\n')
        display.display_text('Options:\n')
        for key, value in cls.HELP_OPTIONS.items():
            value = value + ' '*(16-len(value)) if len(value) < 16 else value
            display.display_text(f'\t{value}\t\t{key}\n')
        return False

    @staticmethod
    def cli_pass(*args):
        return True

cli = Cli()
