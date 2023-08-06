import note.db_setup
from datetime import datetime
from note import crud
from note.display import DisplayModule as display
from note.handler import handle
import uuid
import sys
import readchar
from PyInquirer import prompt
from note.helpers import clear_screen
from note.cli import cli
from time import sleep

clear_screen()
argument_list = sys.argv

# TODO(nirabhra): Add reminders
REV_OPTIONS = {
    'Take a Note': '1',
    'View all Notes': '2',
    'Edit Note': '10',
    'Filter Notes by Tag': '7',
    'View Note': '4',
    'View tags': '6',
    'Delete a Note': '5',
    'Delete a Tag': '8',
    'View all Notes with id': '3',
    'Done for now? - Exit :)': 'q',
}

def interact():
    """
    Interact for user input
    """
    ret_val = True

    questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'What would you like to do?',
            'choices': [key for key, value in REV_OPTIONS.items()]
        },
    ]
    answers = prompt(questions)

    clear_screen()

    # print('selected: ', REV_OPTIONS[answers['choice']])

    ret_val = handle.switch(REV_OPTIONS[answers['choice']])

    return ret_val

if __name__ == '__main__':
    continue_ = True
    while continue_:
        continue_ = interact()

def main():
    """
    Main function
    """
    continue_ = True

    continue_ = cli.evaluate(argument_list[1:])

    if continue_:
        while continue_:
            continue_ = interact()

        clear_screen()