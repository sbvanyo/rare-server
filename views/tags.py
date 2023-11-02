import sqlite3
from models import Tags

def get_all_tags():
    """get all tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM tags t
        """)
        
        tags = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            tag = Tags(row['id'], row['label'])
            tags.append(tag.__dict__)
            
    return tags

def get_single_tag(id):
    """get single tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM tags t
        WHERE t.id = ?
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        tag = Tags(data['id'], data['label'])
        
    return tag.__dict__
