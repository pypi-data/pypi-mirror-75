import sqlite3
import os
import stat

# TODO(nirabhra): change to relative path.
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(DIR_PATH, 'nShells.db')

class DbConnectionError(Exception):
    """
    Database Connection Error
    """
    pass

class GenericError(Exception):
    """
    Generic Error
    """
    pass

def create_connection(db_file):
    """ Create Connection to DB """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        raise GenericError(str(e))

    return conn

def create_table(conn, create_table_sql):
    """ Create Table """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        raise GenericError(str(e))

if not os.path.exists(DB_FILE):
    os.mknod(DB_FILE)
    os.chmod(DB_FILE, 0o640)

conn = create_connection(DB_FILE)
tables = (
    'CREATE TABLE IF NOT EXISTS shells(shell_id TEXT PRIMARY KEY, vision TEXT, \
                                    thought TEXT, tag_name TEXT, created timestamp);',
    'CREATE TABLE IF NOT EXISTS shells_tags(shell_id TEXT, tag_id TEXT);',
    'CREATE TABLE IF NOT EXISTS tags(tag_id TEXT PRIMARY KEY, tag_name TEXT);',
    'CREATE VIRTUAL TABLE IF NOT EXISTS shells_search USING fts5(vision, thought, shell_id);'
)

if conn is not None:
    for table in tables:
        create_table(conn, table)
else:
    raise DbConnectionError('Unable to open storage')
