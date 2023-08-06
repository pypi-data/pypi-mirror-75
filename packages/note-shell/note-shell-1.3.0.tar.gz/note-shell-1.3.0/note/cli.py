from note.handler import handle
from note.display import DisplayModule as display

class Cli(object):
    """
    Cli Module
    """
    HELP_OPTIONS = {
        'Interactive': '-i --interactive',
        'Make a quick note': '-q -qn --quick-note',
        'Make a normal note': '-n --note',
        'List all notes': '-l -ln --list-notes',
        'List all notes in detail': '-ld -lnd --list-notes-detail',
        'List quick notes': '-lq --list-quick-notes',
        'View note': '-v -vn --view-note',
        'Delete a note': '-d -dn --delete-note',
        'List tags': '-lt --list-tags',
        'List notes with tag': '-lnt --list-notes-tag',
        'Delete tag': '-dt --delete-tag',
    }
    CLI_OPTIONS = {
        '-q': 'quicknote',
        '-qn': 'quicknote',
        '--quick-note': 'quicknote',
        '-n': 'normalnote',
        '--note': 'normalnote',
        '-l': 'listnotes',
        '-ln': 'listnotes',
        '--list-notes': 'listnotes',
        '-ld': 'listnotesdetail',
        '-lnd': 'listnotesdetail',
        '--list-notes-detail': 'listnotesdetail',
        '-lq': 'listquicknotes',
        '-list-quick-notes': 'listquicknotes',
        '-v': 'viewnote',
        '-vn': 'viewnote',
        '-view-note': 'viewnote',
        '-d': 'deletenote',
        '-dn': 'deletenote',
        '--delete-note': 'deletenote',
        '-lt': 'listtags',
        '--list-tags': 'listtags',
        '-lnt': 'listnotesfortag',
        '--list-notes-tag': 'listnotesfortag',
        '-dt': 'deletetag',
        '--delete-tag': 'deletetag',
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
    def cli_quicknote(cls, msg, *args, **kwargs):
        # Return true to continue
        if not msg:
            return True

        handle.handle_option_1(title=msg, description=' ', tag_name=cls.QUICKNOTE_TAG)
        return False

    @classmethod
    def cli_normalnote(cls, *args, **kwargs):
        # Return true to continue
        handle.handle_option_1()
        return False

    @staticmethod
    def cli_listnotes(*args, **kwargs):
        # Return true to continue
        handle.handle_option_2()
        return False

    @staticmethod
    def cli_listnotesdetail(*args, **kwargs):
        # Return true to continue
        handle.handle_option_3()
        return False

    @staticmethod
    def cli_viewnote(id_):
        type_ = '2' if id_ else None
        handle.handle_option_4(type_=type_, id_=id_)
        return False

    @staticmethod
    def cli_listnotesfortag(name, *args, **kwargs):
        # Return true to continue
        handle.handle_option_7(name)
        return False

    @classmethod
    def cli_listquicknotes(cls, *args, **kwargs):
        # Return true to continue
        cls.cli_listnotesfortag(cls.QUICKNOTE_TAG)
        return False

    @staticmethod
    def cli_deletenote(id_, *args, **kwargs):
        yes = True if id_ and len(id_.split(' ')) > 1 and id_.split(' ')[1] == '-y' else False
        shell_id = id_.split(' ')[0] if id_ else None
        type_ = '2' if shell_id else None
        handle.handle_option_5(type_=type_, shell_id=shell_id, confirm=yes)
        return False

    @staticmethod
    def cli_listtags(*args, **kwargs):
        handle.handle_option_6()
        return False

    @staticmethod
    def cli_deletetag(name, *args, **kwargs):
        yes = True if name and len(name.split(' ')) > 1 and name.split(' ')[1] == '-y' else False
        name = name.split(' ')[0] if name else None
        type_ = '3' if name else None
        handle.handle_option_8(type_=type_, name=name, confirm=yes)
        return False

    @classmethod
    def cli_help(cls, *args, **kwargs):
        display.display_text('note <option> <input>\n')
        display.display_text('Options:\n')
        for key, value in cls.HELP_OPTIONS.items():
            value = value + ' '*(16-len(value)) if len(value) < 16 else value
            display.display_text(f'\t{value}\t\t{key}\n')

        display.display_text('\n\nNOTE: cli is currenlt supports only single option\n')
        return False

    @staticmethod
    def cli_pass(*args, **kwargs):
        return True

cli = Cli()
