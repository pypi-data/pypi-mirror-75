import note.db_setup
from datetime import datetime
from note import crud
from note.display import DisplayModule as display
from note.handler import handle
import uuid
import sys
from collections import OrderedDict
import readchar

# TODO(nirabhra): Add reminders
OPTIONS = OrderedDict()
OPTIONS['1'] = 'Take a Note'
OPTIONS['2'] = 'View all Notes'
OPTIONS['3'] = 'View all Notes with id'
OPTIONS['4'] = 'View Note <index>(select from list)'
OPTIONS['5'] = 'Delete a Note <index>(select from list)'
OPTIONS['6'] = 'View tags'
OPTIONS['7'] = 'List all Notes for a Tag'
OPTIONS['8'] = 'Delete a Tag <index>(select from list)'
OPTIONS['9'] = 'View notes -> tags'
OPTIONS['q'] = 'Done for now? - Exit :)'

argument_list = sys.argv

def interact():
    """
    Interact for user input
    """
    ret_val = True
    display.display_options(OPTIONS)

    option = readchar.readkey()
    if option == '\x03':
        return False

    ret_val = handle.switch(option)

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