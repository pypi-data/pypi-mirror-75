from datetime import datetime
import uuid
from note import crud
from note.display import DisplayModule as display
import readchar
from PyInquirer import prompt
from note.helpers import clear_screen
from time import sleep

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
    def handle_option_1(cls, title=None, description=None, tag_name=None):
        """
        OPERATION: CREATE
        Take a Note
        """
        if not title and not description and not tag_name:
            display.display_text('* - optional\n')
        if not title:
            display.display_text('Title: ')
            title = str(input())
        else:
            title = str(title)
        if not description:
            display.display_text('Add some description: ')
            description = description or str(input())
        else:
            description = str(description)
        if not tag_name:
            tags = crud.list_tags()
            choices =  ['Create New'] + [t['tag_name'] for t in tags]
            questions = [
                {
                    'type': 'list',
                    'name': 'choice',
                    'message': 'Choose a tag',
                    'choices': choices
                },
            ]
            answers = prompt(questions)

            type_ = answers['choice']

            if type_ == 'Create New':
                display.display_text('*(leave blank for default) Add a tag: ')
                tag_name = tag_name or str(input())
            else:
                tag_name = type_
        else:
            tag_name = str(tag_name)

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

        display.display_text('Note saved, rest assured :)')
        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_2():
        """
        OPERATION: READ
        View all Notes
        """
        shells = crud.list_shells_compact()
        display.display_notes(shells)

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_3():
        """
        OPERATION: READ
        View all Notes with id
        """
        shells = crud.list_shells()
        display.display_notes(shells, include_id=True)

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_4(id_=None):
        """
        TODO(nirabhra): Add option to read by id
        OPERATION: READ
        View Note <id>(select from list)
        """
        if not id_:
            display.display_text('\nEnter id of the note to view: ')
            id_ = str(input())
            clear_screen()
        else:
            id_ = str(id_)

        note = crud.get_shell_from_id(id_)

        display.display_text(f'Vision  :   {note["vision"]}\n')
        display.display_text(f'Thought :   {note["thought"]}\n\n')
        display.display_text(f'Tag : {note["tag_name"]}\n')
        display.display_text(f'Created on {note["created"].split(".")[0]} ; ')
        display.display_text(f'id - {note["shell_id"]}')

        display.display_text('\n\n\n')
        display.display_text('Press any key to continue')
        readchar.readkey()

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_5(type_=None, index=None, shell_id=None, confirm=False):
        """
        OPERATION: DELETE
        Delete a Note
        """
        skip_delete = False

        if not type_:
            options = {
                'Delete by id': '2',
                'Delete by index': '1',
            }
            questions = [
                {
                    'type': 'list',
                    'name': 'choice',
                    'message': 'Welcome! How may I help you?',
                    'choices': [key for key, value in options.items()]
                },
            ]
            answers = prompt(questions)

            type_ = options[answers['choice']]
        else:
            type_ = str(type_)

        if str(type_) == '1':
            if not index:
                display.display_text('Enter index of the note to delete: ')
                index = int(input())
            else:
                index = int(index)

            note = crud.get_shell_by_offset(index - 1)
            shell_id = note['shell_id']
        elif str(type_) == '2':
            if not shell_id:
                display.display_text('Enter id of the note to delete: ')
                shell_id = str(input())
            else:
                shell_id = str(shell_id)

            note = crud.get_shell_from_id(shell_id)
        else:
            display.display_text('Only 1 / 2 are valid delete choices .. aborting delete\n')
            skip_delete = True

        if shell_id and not skip_delete:
            key = 'n'
            if not confirm:
                vision_hint = note['vision'] if len(note['vision']) <= 25 else ''.join([note['vision'][:23], '...'])
                display.display_text(f'\nAre you sure to delete {vision_hint} ?\n')
                display.display_text(f'\nPress y to continue deletion ')
                key = readchar.readkey()
                display.display_text(f'\n')

            if key == 'y' or key == 'Y' or confirm:
                crud.delete_shell(shell_id)
                tag = crud.get_tag_by_name(note['tag_name'])
                crud.delete_shell_tag((shell_id, tag['tag_id']))
                display.display_text('Deleted successfully')
            else:
                display.display_text('Aborting ..')
        elif not skip_delete:
            display.display_text('Note not found !')

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_6():
        """
        OPERATION: READ
        View all tags
        """
        tags = crud.list_tags()
        display.display_tags(tags)

        display.display_text('\n')

        return True

    @staticmethod
    def handle_option_7(name=None):
        """
        OPERATION: READ
        List all Notes for a Tag
        """
        if not name:
            display.display_text('Enter tag name: ')
            name = str(input())
        else:
            name = str(name)

        tag = crud.get_tag_by_name(name)

        shell_ids = crud.get_shell_ids_from_tag_id(tag['tag_id'])

        shells = crud.get_shell_from_ids(shell_ids)
        display.display_notes(shells)

        display.display_text('\n')

        return True

    @classmethod
    def handle_option_8(cls, type_=None, index=None, tag_id=None, name=None, confirm=False):
        """
        OPERATION: DELETE
        Delete a Tag <index>(select from list)
        """
        skip_delete = False

        if not type_:
            options = {
                'Delete by name': '3',
                'Delete by id': '2',
                'Delete by index': '1',
            }
            questions = [
                {
                    'type': 'list',
                    'name': 'choice',
                    'message': 'Welcome! How may I help you?',
                    'choices': [key for key, value in options.items()]
                },
            ]
            answers = prompt(questions)

            type_ = options[answers['choice']]
        else:
            type_ = str(type_)

        if str(type_) == '1':
            if not index:
                display.display_text('Enter index of the tag to delete: ')
                index = int(input())
            else:
                index = int(index)

            tag = crud.get_tag_from_offset(index - 1)
            tag_id = tag['tag_id']
        elif str(type_) == '2':
            if not tag_id:
                display.display_text('Enter id of the tag to delete: ')
                tag_id = str(input())
            else:
                tag_id = str(tag_id)

            tag = crud.get_tag_from_id(tag_id)
        elif str(type_) == '3':
            if not name:
                display.display_text('Enter name of the tag to delete: ')
                name = str(input())
            else:
                name = str(name)

            tag = crud.get_tag_by_name(name)
            tag_id = tag['tag_id']
        else:
            display.display_text('Only 1 / 2 are valid delete choices .. aborting delete\n')
            skip_delete = True

        if tag_id and not skip_delete:
            # Delete tag
            key = 'n'
            skip_note_delete = False
            tag_hint = tag['tag_name'] if len(tag['tag_name']) <= 25 else ''.join([tag['tag_name'][:23], '...'])
            associated_shell_ids = crud.get_shell_ids_from_tag_id(tag_id)

            if not confirm:
                display.display_text(f'\nAre you sure to delete tag "{tag_hint}" ?\n')
                display.display_text(f'Press y to continue deletion ')
                key = readchar.readkey()
                display.display_text(f'\n')

            if key == 'y' or key == 'Y' or confirm:
                crud.delete_tag(tag_id)
                crud.delete_shell_tag_from_tag((tag_id))
                display.display_text('\nTag deleted successfully')
            else:
                skip_note_delete = True
                display.display_text('\nAborting ..\n')

            # Delete associated notes
            key = 'n'

            if not confirm:
                display.display_text(f'\nDelete associated notes?\n')
                display.display_text(f'Press y to continue deletion ')
                key = readchar.readkey()
                display.display_text(f'\n')

            if (key == 'y' or key == 'Y' or confirm) and not skip_note_delete:
                crud.delete_shell_by_tag_name(tag['tag_name'])
                display.display_text('\nNotes deleted successfully')
            elif not skip_note_delete:
                default_tag = crud.get_tag_by_name(cls._default_tag_name)

                for shell_id in associated_shell_ids:
                    crud.create_shell_tag((shell_id, default_tag['tag_id']))

                crud.update_shell_update_tag_to_default(tag['tag_name'], updated_name=cls._default_tag_name)

                display.display_text('\nNot deleting associated notes ..')

        elif not skip_delete:
            display.display_text('\nNote not found !')

        display.display_text('\n')

        return True

    @staticmethod
    def _handle_option_9():
        """
        Not accesible via console !
        OPERATION: READ
        View all shell_tags
        """
        shell_tags = crud.list_shell_tags()
        display.display_shell_tags(shell_tags)

        display.display_text('\n')

        return True

    @classmethod
    def handle_option_q(cls):
        """
        Done for now? - Exit :)
        """
        farewell_text = 'Thankyou for using notes!\nBye 🖐'

        total_animation_time = 1.5
        animation_speed = total_animation_time / len(farewell_text)
        for i in range(0, len(farewell_text)):
            display.display_text(farewell_text[i])
            sleep(animation_speed)

        sleep(0.75)

        return False

    @staticmethod
    def incorrect_option():
        display.display_text('Incorrect option selected, exiting !!!')

        display.display_text('\n')

        return False

handle = Handle()
