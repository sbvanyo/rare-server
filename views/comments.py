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
            comment = Comment(row['id'], row['author_id'],
                              row['post_id'], row['content'])

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
        """, (id, ))
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


def get_comments_for_post(post_id):
    """GET COMMENTS FOR A SPECIFIC POST"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id as comment_id,
            c.author_id,
            c.post_id,
            c.content,
            u.id as user_id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Comments c
        INNER JOIN Posts p ON c.post_id = p.id
        LEFT JOIN Users u ON c.author_id = u.id
        WHERE p.id = ?
        """, (post_id, ))

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment_data = {
                'comment_id': row['comment_id'],
                'author_id': row['author_id'],
                'post_id': row['post_id'],
                'content': row['content'],
                'user': {
                    'id': row['user_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'bio': row['bio'],
                    'username': row['username'],
                    'password': row['password'],
                    'profile_image_url': row['profile_image_url'],
                    'created_on': row['created_on'],
                    'active': row['active']
                }
            }

            comments.append(comment_data)

    return comments
