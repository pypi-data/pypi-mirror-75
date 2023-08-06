from note.db_setup import conn
from datetime import datetime

def create_shell(data):
    """ Db shells : Create Shell """

    query = 'INSERT INTO shells(shell_id, vision, thought, tag_name, created) VALUES(?, ?, ?, ?, ?);'
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def create_tag(data):
    """ Db tags : Create Tag """

    query = 'INSERT INTO tags(tag_id, tag_name) VALUES(?, ?);'
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def list_shells():
    """ Db shells : List All Shells """

    query = 'SELECT shell_id, vision, thought, tag_name, created FROM shells;'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'shell_id': row[0],
            'vision': row[1],
            'thought': row[2],
            'tag_name': row[3],
            'created': row[4],
        })
    return data

def list_shells_compact():
    """ Db shells : List All Shells """
    query = 'SELECT vision, thought, tag_name, created FROM shells;'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'vision': row[0],
            'thought': row[1],
            'tag_name': row[2],
            'created': row[3],
        })
    return data

def list_tags():
    """ Db tags : List All Tags """

    query = 'SELECT DISTINCT tag_name FROM shells;'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'tag_name': row[0],
        })
    return data

def get_shell_by_offset(offset):
    """ Db shells : Get nth row of shells """

    query = f'SELECT shell_id, vision, thought, tag_name, created FROM shells LIMIT 1 OFFSET {str(offset)};'
    cur = conn.cursor()
    cur.execute(query)
    data = None
    for row in cur:
        data = {
            'shell_id': row[0],
            'vision': row[1],
            'thought': row[2],
            'tag_name': row[3],
            'created': row[4],
        }
        break

    return data

def get_shell_from_ids(id_list=None):
    """ Db shells : Get shell from id_list """

    id_list = id_list if id_list and (isinstance(id_list, list) or isinstance(id_list, tuple)) else ()
    id_list = [id.join(['"', '"']) for id in id_list]
    query = f'SELECT shell_id, vision, thought, tag_name, created \
                                FROM shells WHERE shell_id IN ({",".join(id_list)})\
                                ORDER BY created ASC;'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'shell_id': row[0],
            'vision': row[1],
            'thought': row[2],
            'tag_name': row[3],
            'created': row[4],
        })

    return data

def get_shell_from_id(id=''):
    """ Db shells : Get shell from id """

    query = f'SELECT shell_id, vision, thought, tag_name, created FROM shells WHERE shell_id="{id}";'
    cur = conn.cursor()
    cur.execute(query)
    data = None
    for row in cur:
        data = {
            'shell_id': row[0],
            'vision': row[1],
            'thought': row[2],
            'tag_name': row[3],
            'created': row[4],
        }
        break

    return data

def get_shells_from_tag(tag):
    """ Db shells : Get shells from tag """

    query = f'SELECT shell_id, vision, thought, tag_name, created FROM shells WHERE tag_name="{tag}";'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'shell_id': row[0],
            'vision': row[1],
            'thought': row[2],
            'tag_name': row[3],
            'created': row[4],
        })

    return data

def get_shell_ids_from_tag_name(name):
    """ Db shells : Get all shell ids associated with a tag name """

    query = f'SELECT shell_id FROM shells WHERE tag_name="{name}";'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append(row[0])

    return data

def update_shell_update_tag_to_default(tag_name, updated_name='default'):
    """ Db shells : Update Shell """

    query = f'UPDATE shells SET tag_name="{updated_name}" WHERE tag_name="{tag_name}";'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return cur.lastrowid

def update_shell(id_, vision, thought, tag):
    """ Db shells : Update Shell """

    query = f'UPDATE shells SET vision=?, thought=?, tag_name=?, created=? WHERE shell_id=?;'
    cur = conn.cursor()
    cur.execute(query, (vision, thought, tag, datetime.now(), id_))
    conn.commit()
    return cur.lastrowid

def delete_shell(id):
    """ Db shells : Delete Shell """

    query = f'DELETE FROM shells WHERE shell_id="{id}";'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return cur.lastrowid

def delete_shell_by_tag_name(name):
    """ Db shells : Delete Shell """

    query = f'DELETE FROM shells WHERE tag_name="{name}";'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return cur.lastrowid

# Ft5 table for search

def create_shell_search(data):
    """ Db shells_search : Save entry to Shell Search """

    query = 'INSERT INTO shells_search(vision, thought, shell_id) VALUES(?, ?, ?);'
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def update_shell_search(id_, vision, thought):
    """ Db shells_search : Update Shell Search """

    query = f'UPDATE shells_search SET vision=?, thought=? WHERE shell_id=?;'
    cur = conn.cursor()
    cur.execute(query, (vision, thought, id_))
    conn.commit()
    return cur.lastrowid

def delete_shell_search(id_):
    """ Db shells_search : Delete Shell Search """

    query = f'DELETE FROM shells_search WHERE shell_id=?;'
    cur = conn.cursor()
    cur.execute(query, [id_])
    conn.commit()
    return cur.lastrowid

def delete_shell_search_by_tag_name(name):
    """ Db shells_search : Delete Shell Search """

    query = '''
                DELETE FROM shells_search WHERE shell_id IN (
                    SELECT shell_id FROM shells WHERE tag_name=?
                );
            '''
    cur = conn.cursor()
    cur.execute(f'SELECT shell_id FROM shells WHERE tag_name={name};')
    print('result 1: ', cur.lastrowid)
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM shells_search WHERE shell_id IN (SELECT shell_id FROM shells WHERE tag_name={name});')
    print('result 2: ', cur.lastrowid)
    cur = conn.cursor()
    cur.execute(query, [name])
    conn.commit()
    return cur.lastrowid

def search_shell(text):
    """ Db shells_search : Search in shells for text """
    print('text to match: ', text)
    query = f'''SELECT shell_id, vision, thought, tag_name, created FROM shells WHERE shell_id IN
                (
                    SELECT shell_id FROM shells_search
                    WHERE vision MATCH ? OR thought MATCH ? ORDER BY rank
                ) ORDER BY created ASC;'''
    cur = conn.cursor()
    cur.execute(query, (text, text))
    data = []
    for row in cur:
        data.append({
            'shell_id': row[0],
            'vision': row[1],
            'thought': row[2],
            'tag_name': row[3],
            'created': row[4],
        })
    return data
