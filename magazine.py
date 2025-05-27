from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._id = id
        self._name = None
        self._category = None
        self.name = name
        self.category = category

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

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a non-empty string")
        self._category = value.strip()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self._id is None:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?) RETURNING id",
                    (self.name, self.category)
                )
                self._id = cursor.fetchone()['id']
                conn.commit()
            else:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Failed to save magazine: {e}")
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?", (id,))
            row = cursor.fetchone()
            return cls(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, category FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
            return cls(row['name'], row['category'], row['id']) if row else None
        finally:
            conn.close()

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT title FROM articles WHERE magazine_id = ?",
                (self.id,)
            )
            rows = cursor.fetchall()
            print(f"DEBUG: Article titles for magazine_id={self.id}: {rows}")
            return [row['title'] for row in rows]
        finally:
            conn.close()

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT DISTINCT a.id, a.name
                FROM authors a
                JOIN articles art ON a.id = art.author_id
                WHERE art.magazine_id = ?
                """,
                (self.id,)
            )
            return [{'id': row['id'], 'name': row['name']} for row in cursor.fetchall()]
        finally:
            conn.close()

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT a.id, a.name
                FROM authors a
                JOIN articles art ON a.id = art.author_id
                WHERE art.magazine_id = ?
                GROUP BY a.id, a.name
                HAVING COUNT(art.id) > 2
                """,
                (self.id,)
            )
            return [{'id': row['id'], 'name': row['name']} for row in cursor.fetchall()]
        finally:
            conn.close()