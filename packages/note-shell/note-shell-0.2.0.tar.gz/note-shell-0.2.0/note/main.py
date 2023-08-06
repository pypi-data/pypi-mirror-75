import note.db_setup
from datetime import datetime
from note import crud
from note.display import DisplayModule as display
from note.handler import handle
import uuid
import sys
import readchar
from PyInquirer import prompt
from pprint import pprint
from os import system, name

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

clear_screen()

# TODO(nirabhra): Add reminders
REV_OPTIONS = {
    'Take a Note': '1',
    'View all Notes': '2',
    'View all Notes with id': '3',
    'View Note <index>': '4',
    'Delete a Note <index>': '5',
    'View tags': '6',
    'List all Notes for a Tag': '7',
    'Delete a Tag <index>': '8',
    'Done for now? - Exit :)': 'q',
}

argument_list = sys.argv

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
    while continue_:
        continue_ = interact()