""" Comments Module """
import sqlite3
import json
from models import Comment

def get_all_comments():
    """GET ALL COMMENTS"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content
        FROM Comments c
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['author_id'], row['post_id'], row['content'])

            comments.append(comment.__dict__)

    return comments

def get_single_comment(id):
    """GET SINGLE COMMENT"""
    with sqlite3.connect("./db.sqlite3") as conn:
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

        comment = Comment(
            data['id'],
            data['author_id'],
            data['post_id'],
            data['content'])
        return comment.__dict__


def create_comment(new_comment):
    """CREATE COMMENT"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( author_id, post_id, content )
        VALUES
            ( ?, ?, ?);
            """, (new_comment['author_id'], new_comment['post_id'], new_comment['content'], ))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return new_comment

def delete_comment(id):
    """DELETE COMMENT"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))

def update_comment(id, new_comment):
    """UPDATE COMMENT"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Comments
        SET
            author_id = ?,
            post_id = ?,
            content = ?
        WHERE id = ?
        """, (new_comment['author_id'], new_comment['post_id'], new_comment['content'], id))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
