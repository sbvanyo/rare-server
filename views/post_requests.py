import sqlite3
import json
from models import Post, User, Tags

def update_post(id, new_post):
    """docstrings"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?
        """, (
                new_post['user_id'],
                new_post['category_id'],
                new_post['title'],
                new_post['publication_date'],
                new_post['image_url'],
                new_post['content'],
                new_post['approved'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def delete_post(id):
    """docstring"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE 
        FROM Posts
        WHERE id = ?
        """, (id, ))

def get_single_post(id):
    """docstring"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor2 = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Posts p
        JOIN Users u
        ON p.user_id = u.id
        WHERE p.id = ?
        """, ( id, ))
        
        db_cursor2.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id,
            t.id,
            t.label
            
        FROM PostTags pt
        JOIN tags t
            on pt.tag_id = t.id
        WHERE pt.post_id = ?
        """, ( id, ))

        # Load the single result into memory
        tags = []
        data = db_cursor.fetchone()
        dataset = db_cursor2.fetchall()
        for row in dataset:
            tag = Tags(row['id'], row['label'])
            tags.append(tag.__dict__)
        # Create an post instance from the current row
        post = Post(data['id'],
                     data['user_id'],
                     data['category_id'],
                     data['title'],
                     data['publication_date'],
                     data['image_url'],
                     data['content'],
                     data['approved'])
        
        user = User(data['id'], data['first_name'], data['last_name'], data['email'], data['bio'], data['username'], data['password'], data['profile_image_url'], data['created_on'], data['active'])
        
        post.user = user.__dict__
        post.tags = tags
        
        return post.__dict__

def get_all_posts():
    """docstring"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Posts p
        JOIN Users u
        ON p.user_id = u.id
        """)

        # Initialize an empty list to hold all post representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an post instance from the current row
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'],
                            row['image_url'], row['content'], row['approved'])
            
            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
            
            post.user = user.__dict__

            # Add the dictionary representation of the post to the list
            posts.append(post.__dict__)

    return posts

def create_post(new_post):
    """docstring"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (
            new_post['user_id'],
            new_post['category_id'],
            new_post['title'],
            new_post['publication_date'],
            new_post['image_url'],
            new_post['content'],
            new_post['approved'] ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the post dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id


    return new_post
