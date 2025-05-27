from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author=None, magazine=None, id=None):
        self._id = id
        self._title = None
        self._author = None
        self._magazine = None
        self.title = title
        if author:
            self.author = author
        if magazine:
            self.magazine = magazine

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string")
        self._title = value.strip()

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        from lib.models.author import Author
        if not isinstance(value, Author) or not value.id:
            raise ValueError("Author must be a saved Author instance")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        from lib.models.magazine import Magazine
        if not isinstance(value, Magazine) or not value.id:
            raise ValueError("Magazine must be a saved Magazine instance")
        self._magazine = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self._id is None:
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?) RETURNING id",
                    (self.title, self.author.id, self.magazine.id)
                )
                self._id = cursor.fetchone()['id']
                print(f"DEBUG: Saved article id={self._id}, title={self.title}")
                conn.commit()
            else:
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self.title, self.author.id, self.magazine.id, self.id)
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"DEBUG: Failed to save article: {e}")
            raise RuntimeError(f"Failed to save article: {e}")
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE id = ?", (id,))
            row = cursor.fetchone()
            if not row:
                print(f"DEBUG: No article found for id={id}")
                return None
            from lib.models.author import Author
            from lib.models.magazine import Magazine
            author = Author.find_by_id(row['author_id'])
            magazine = Magazine.find_by_id(row['magazine_id'])
            if not author or not magazine:
                print(f"DEBUG: Invalid author_id={row['author_id']} or magazine_id={row['magazine_id']} for article id={id}")
                return None
            article = cls(row['title'], author, magazine, row['id'])
            print(f"DEBUG: Found article id={id}, title={row['title']}")
            return article
        finally:
            conn.close()

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE title = ?", (title,))
            row = cursor.fetchone()
            if not row:
                return None
            from lib.models.author import Author
            from lib.models.magazine import Magazine
            author = Author.find_by_id(row['author_id'])
            magazine = Magazine.find_by_id(row['magazine_id'])
            if not author or not magazine:
                return None
            return cls(row['title'], author, magazine, row['id'])
        finally:
            conn.close()