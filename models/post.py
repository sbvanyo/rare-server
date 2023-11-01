from datetime import datetime
class Post():
    """wow"""

    def __init__(self, id, user_id, category_id, title,
                 publication_date, image_url, content, approved):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.title = title
        self.publication_date = datetime.now()
        self.image_url = image_url
        self.content = content
        self.approved = approved

with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

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
            p.approved
        FROM Post p
        WHERE p.id = ?
        """, ( id, ))
