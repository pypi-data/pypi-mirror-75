from datetime import datetime
import uuid
from note import crud
from note.display import DisplayModule as display
import readchar

class Handle(object):
    """
    Handle Module
    """
    _default_tag_name = 'default'

    def __init__(self):
        tag_id = str(uuid.uuid4()).replace('-', '')
        tag_data = (tag_id, self._default_tag_name)

        tag = crud.get_tag_by_name(self._default_tag_name)
        if not tag:
            crud.create_tag(tag_data)

    @classmethod
    def switch(cls, option, *args):
        return getattr(cls, 'handle_option_' + str(option), cls.incorrect_option)(*args)

    @classmethod
    def handle_option_1(cls):
        """
        OPERATION: CREATE
        Take a Note
        """
        title_text = 'Enter Title:'
        display.display_text(f'\n{"~"*len(title_text)}\n{title_text} ')
        title = str(input())
        display.display_text('Enter Description: ')
        description = str(input())
        display.display_text('Enter Tag(blank if no tag): ')
        tag_name = str(input()) # TODO: have functionality for blank tag

        if tag_name == '' or tag_name == None:
            tag_name = cls._default_tag_name

        time = datetime.now()
        shell_id = str(uuid.uuid4()).replace('-', '')
        tag_id = str(uuid.uuid4()).replace('-', '')
        shell_data = (shell_id, title, description, tag_name, time)
        tag_data = (tag_id, tag_name)

        crud.create_shell(shell_data)
        tag = crud.get_tag_by_name(tag_name)
        if tag:
            tag_id = tag['tag_id']
        else:
            crud.create_tag(tag_data)
        crud.create_shell_tag((shell_id, tag_id))

        display.display_text('Note saved, rest assured :)\n')
        return True

    @staticmethod
    def handle_option_2():
        """
        OPERATION: READ
        View all Notes
        """
        shells = crud.list_shells_compact()
        display.display_notes(shells)
        return True

    @staticmethod
    def handle_option_3():
        """
        OPERATION: READ
        View all Notes with id
        """
        shells = crud.list_shells()
        display.display_notes(shells, include_id=True)
        return True

    @staticmethod
    def handle_option_4():
        """
        TODO(nirabhra): Add option to read by id
        OPERATION: READ
        View Note <index>(select from list)
        """
        display.display_text('\nEnter index of the note to view: ')
        index = int(input())

        note = crud.get_shell_by_offset(index - 1)

        display.display_text(f'\n{"~"*50}\n')
        display.display_text(f'Vision:    {note["vision"]}\n\n')
        display.display_text(f'Thought:   {note["thought"]}\n\n')
        display.display_text(f'Tag:       {note["tag_name"]}\n\n')
        display.display_text(f'Timestamp: {note["created"].split(".")[0]}')

        display.display_text('\n\n\n')
        display.display_text('Press any key to continue')
        readchar.readkey()
        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_5():
        """
        OPERATION: DELETE
        Delete a Note
        """
        skip_delete = False

        display.display_text('\nDelete by index - press 1')
        display.display_text('\nDelete by id    - press 2 ')
        type_ = readchar.readkey()

        if str(type_) == '1':
            display.display_text('\nEnter index of the note to delete: ')
            index = int(input())

            note = crud.get_shell_by_offset(index - 1)
            shell_id = note['shell_id']
        elif str(type_) == '2':
            display.display_text('\nEnter id of the note to delete: ')
            shell_id = str(input())
            note = crud.get_shell_from_id(shell_id)
        else:
            display.display_text('\nOnly 1 / 2 are valid delete choices .. aborting delete\n')
            skip_delete = True

        if shell_id and not skip_delete:
            vision_hint = note['vision'] if len(note['vision']) <= 25 else ''.join([note['vision'][:23], '...'])
            display.display_text(f'\nAre you sure to delete {vision_hint} ?\n')
            display.display_text(f'\nPress y to continue deletion ')
            key = readchar.readkey()
            display.display_text(f'\n')
            if key == 'y' or key == 'Y':
                crud.delete_shell(shell_id)
                tag = crud.get_tag_by_name(note['tag_name'])
                x = crud.delete_shell_tag((shell_id, tag['tag_id']))
                display.display_text('\nDeleted successfully')
            else:
                display.display_text('\nAborting ..\n')
        elif not skip_delete:
            display.display_text('\nNote not found !\n')

        return True

    @staticmethod
    def handle_option_6():
        """
        OPERATION: READ
        View all tags
        """
        tags = crud.list_tags()
        display.display_tags(tags)
        return True

    @staticmethod
    def handle_option_7():
        """
        OPERATION: READ
        List all Notes for a Tag
        """
        display.display_text('\nEnter tag name: ')
        name = str(input())

        tag = crud.get_tag_by_name(name)

        shell_ids = crud.get_shell_ids_from_tag_id(tag['tag_id'])

        shells = crud.get_shell_from_ids(shell_ids)
        display.display_notes(shells)

        return True

    @classmethod
    def handle_option_8(cls):
        """
        OPERATION: DELETE
        Delete a Tag <index>(select from list)
        """
        skip_delete = False

        display.display_text('\nDelete by index - press 2')
        display.display_text('\nDelete by id    - press 1 ')
        display.display_text('\nDelete by name    - press 3 ')
        type_ = readchar.readkey()

        if str(type_) == '1':
            display.display_text('\nEnter index of the tag to delete: ')
            index = int(input())

            tag = crud.get_tag_from_offset(index - 1)
            tag_id = tag['tag_id']
        elif str(type_) == '2':
            display.display_text('\nEnter id of the tag to delete: ')
            tag_id = str(input())
            tag = crud.get_tag_from_id(tag_id)
        elif str(type_) == '3':
            display.display_text('\nEnter name of the tag to delete: ')
            name = str(input())
            tag = crud.get_tag_by_name(name)
            tag_id = tag['tag_id']
        else:
            display.display_text('\nOnly 1 / 2 are valid delete choices .. aborting delete\n')
            skip_delete = True

        if tag_id and not skip_delete:
            # Delete tag
            skip_note_delete = False
            tag_hint = tag['tag_name'] if len(tag['tag_name']) <= 25 else ''.join([tag['tag_name'][:23], '...'])
            associated_shell_ids = crud.get_shell_ids_from_tag_id(tag_id)

            display.display_text(f'\nAre you sure to delete tag "{tag_hint}" ?\n')
            display.display_text(f'Press y to continue deletion ')

            key = readchar.readkey()
            display.display_text(f'\n')

            if key == 'y' or key == 'Y':
                crud.delete_tag(tag_id)
                crud.delete_shell_tag_from_tag((tag_id))
                display.display_text('\nTag deleted successfully')
            else:
                skip_note_delete = True
                display.display_text('\nAborting ..\n')


            # Delete associated notes
            display.display_text(f'\nDelete associated notes?\n')
            display.display_text(f'Press y to continue deletion ')
            key = readchar.readkey()
            display.display_text(f'\n')
            if (key == 'y' or key == 'Y') and not skip_note_delete:
                crud.delete_shell_by_tag_name(tag['tag_name'])
                display.display_text('\nNotes deleted successfully')
            elif not skip_note_delete:
                default_tag = crud.get_tag_by_name(cls._default_tag_name)

                for shell_id in associated_shell_ids:
                    crud.create_shell_tag((shell_id, default_tag['tag_id']))

                crud.update_shell_update_tag_to_default(tag['tag_name'], updated_name=cls._default_tag_name)

                display.display_text('\nNot deleting associated notes ..\n')

        elif not skip_delete:
            display.display_text('\nNote not found !\n')

        return True

    @staticmethod
    def handle_option_9():
        """
        OPERATION: READ
        View all shell_tags
        """
        shell_tags = crud.list_shell_tags()
        display.display_shell_tags(shell_tags)
        return True

    @classmethod
    def handle_option_q(cls):
        """
        Done for now? - Exit :)
        """
        display.display_text('\nYour notes are saved safely, keep taking notes! Bye ..\n')
        return False

    @staticmethod
    def incorrect_option():
        display.display_text('\nIncorrect option selected, exiting !!!\n')
        return False

handle = Handle()
