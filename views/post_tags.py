import sqlite3
from models import Post_tags


def get_all_post_tags():
    """get all post_tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id
        FROM PostTags pt
        """)

        post_tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post_tag = Post_tags(row['id'], row['post_id'], row['tag_id'])

            post_tags.append(post_tag.__dict__)

    return post_tags


def get_single_post_tag(id):
    """get single post_tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id
        FROM PostTags pt
        WHERE pt.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        post_tag = Post_tags(data['id'], data['post_id'], data['tag_id'])

        return post_tag.__dict__


def add_tag_to_post(new_post_tag):
    """adding a tag to a post"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostTags
            ( post_id, tag_id )
        VALUES
            ( ?, ? );
        """, (new_post_tag['post_id'], new_post_tag['tag_id'], ))

        id = db_cursor.lastrowid

        new_post_tag['id'] = id

    return new_post_tag


def remove_tag_from_post(id):
    """removing a tag from a post"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM PostTags
        WHERE id = ?
        """, (id, ))
