from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self._id = id
        self._name = None
        self.name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self._id is None:
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?) RETURNING id",
                    (self.name,)
                )
                self._id = cursor.fetchone()['id']
                conn.commit()
            else:
                cursor.execute(
                    "UPDATE authors SET name = ? WHERE id = ?",
                    (self.name, self.id)
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Failed to save author: {e}")
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name FROM authors WHERE id = ?", (id,))
            row = cursor.fetchone()
            return cls(row['name'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
            return cls(row['name'], row['id']) if row else None
        finally:
            conn.close()

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM articles WHERE author_id = ?",
                (self.id,)
            )
            rows = cursor.fetchall()
            print(f"DEBUG: Articles for author_id={self.id}: {rows}")
            return [Article.find_by_id(row['id']) for row in rows if Article.find_by_id(row['id'])]
        finally:
            conn.close()

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT DISTINCT m.id, m.name
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
                """,
                (self.id,)
            )
            rows = cursor.fetchall()
            print(f"DEBUG: Magazines for author_id={self.id}: {rows}")
            return [{'id': row['id'], 'name': row['name']} for row in rows]
        finally:
            conn.close()

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title, self, magazine)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT DISTINCT m.category
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
                """,
                (self.id,)
            )
            return [row['category'] for row in cursor.fetchall()]
        finally:
            conn.close()