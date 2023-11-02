import sqlite3
# import json
from models import Comments

COMMENTS = [
    
]

def get_all_comments():
    """GET ALL COMMENTS"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute(""" 
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content
        FROM Comment c
        """)
        comments = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            comment = Comments(row['id'], row['author_id'], row['post_id'], row['content'])
            
            comments.append(comment.__dict__)
            
    return comments

def get_single_comment(id):
    """GET SINGLE COMMENT"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(""" 
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content
        FROM comment c
        WHERE c.id = ?
        """, ( id, ))
        data = db_cursor.fetchone()
        
        comment = Comments(
            data['id'],
            data['author_id'],
            data['post_id'],
            data['content'])
        return comment.__dict__


def create_comment(new_comment):
    """CREATE COMMENT"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute(""" 
        INSERT INTO Comment
            ( author_id, post_id, content )
        VALUES
            ( ?, ?, ?);
            """, (new_comment['author_id'], new_comment['post_id'], new_comment['content'], ))
    
        id = db_cursor.lastrowid
        
        new_comment['id'] = id
    
    return new_comment

def delete_comment(id):
    """DELETE COMMENT"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute(""" 
        DELETE FROM comment
        WHERE id = ?
        """, (id, ))
    
