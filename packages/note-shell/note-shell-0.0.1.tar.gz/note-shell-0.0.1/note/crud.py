from note.db_setup import conn

def create_shell(data):
    """
    DB: shells
    Create Shell
    """
    query = 'INSERT INTO shells(shell_id, vision, thought, tag_name, created) VALUES(?, ?, ?, ?, ?);'
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def create_shell_tag(data):
    """
    DB: shells_tags
    Create Shell Tag
    """
    query = 'INSERT INTO shells_tags(shell_id, tag_id) VALUES(?, ?);'
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def create_tag(data):
    """
    DB: tags
    Create Tag
    """
    query = 'INSERT INTO tags(tag_id, tag_name) VALUES(?, ?);'
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def list_shells():
    """
    DB: shells
    List All Shells
    """
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
    """
    DB: shells
    List All Shells
    """
    query = 'SELECT vision, thought, tag_name FROM shells;'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'vision': row[0],
            'thought': row[1],
            'tag_name': row[2],
        })
    return data

def list_tags():
    """
    DB: tags
    List All Tags
    """
    query = 'SELECT tag_id, tag_name FROM tags;'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'tag_id': row[0],
            'tag_name': row[1],
        })
    return data

def list_shell_tags():
    """
    DB: tags
    List All Tags
    """
    query = 'SELECT shell_id, tag_id FROM shells_tags;'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'shell_id': row[0],
            'tag_id': row[1],
        })
    return data

def get_shell_by_offset(offset):
    """
    DB: shells
    Get nth row of shells
    """
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
    """
    DB: shells
    Get shell from id_list
    """
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
    """
    DB: shells
    Get shell from id
    """
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

def get_tag_by_name(name):
    """
    DB: tags
    Get nth row of tags
    """
    query = f'SELECT tag_id, tag_name FROM tags WHERE tag_name="{name}";'
    cur = conn.cursor()
    cur.execute(query)
    data = None
    for row in cur:
        data = {
            'tag_id': row[0],
            'tag_name': row[1],
        }
        break

    return data

def get_tag_from_offset(offset):
    """
    DB: tags
    Get nth row of tags
    """
    query = f'SELECT tag_id, tag_name FROM tags LIMIT 1 OFFSET {str(offset)};'
    cur = conn.cursor()
    cur.execute(query)
    data = None
    for row in cur:
        data = {
            'tag_id': row[0],
            'tag_name': row[1],
        }
        break

    return data

def get_tag_from_id(id=''):
    """
    DB: tags
    Get tags from id
    """
    query = f'SELECT tag_id, tag_name FROM tags WHERE tag_id="{id}";'
    cur = conn.cursor()
    cur.execute(query)
    data = None
    for row in cur:
        data = {
            'tag_id': row[0],
            'tag_name': row[1],
        }
        break

    return data

def get_shell_ids_from_tag_id(id):
    """
    DB: shells_tags
    Get all shell ids associated to a tag
    """
    query = f'SELECT shell_id FROM shells_tags WHERE tag_id="{id}";'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append(row[0])

    return data

def get_shell_ids_from_tag_name(name):
    """
    DB: shells
    Get all shell ids associated with a tag name
    """
    query = f'SELECT shell_id FROM shells WHERE tag_name="{name}";'
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append(row[0])

    return data

def update_shell_update_tag_to_default(tag_name, updated_name='default'):
    """
    DB: shells
    Update Shell
    """
    query = f'UPDATE shells SET tag_name="{updated_name}" WHERE tag_name="{tag_name}";'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return cur.lastrowid

def delete_shell(id):
    """
    DB: shells
    Delete Shell
    """
    query = f'DELETE FROM shells WHERE shell_id="{id}";'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return cur.lastrowid

def delete_shell_by_tag_name(name):
    """
    DB: shells
    Delete Shell
    """
    query = f'DELETE FROM shells WHERE tag_name="{name}";'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return cur.lastrowid

# def delete_shell_tag(shell_id, tag_id):
def delete_shell_tag(data):
    """
    DB: shells_tags
    Delete shell tag
    """
    query = 'DELETE FROM shells_tags WHERE shell_id=? AND tag_id=?;'
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def delete_shell_tag_from_tag(id):
    """
    DB: shells_tags
    Delete shell tag
    """
    query = f'DELETE FROM shells_tags WHERE tag_id="{id}";'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return cur.lastrowid

def delete_tag(id):
    """
    DB: tags
    Delete Tag
    """
    query = f'DELETE FROM tags WHERE tag_id="{id}";'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return cur.lastrowid
