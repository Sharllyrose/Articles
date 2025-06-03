class Magazine:
    all_magazines = []

    def __init__(self, name, category):
        self._name = name
        self._category = category
        Magazine.all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @classmethod
    def all(cls):
        return cls.all_magazines

    def __eq__(self, other):
        if not isinstance(other, Magazine):
            return False
        return self.name == other.name and self.category == other.category

    def __hash__(self):
        return hash((self.name, self.category))

    def contributors(self):
        # Return unique list of Author instances who have written for this magazine
        authors = set()
        from article import Article
        for article in Article.all():
            if article.magazine == self:
                authors.add(article.author)
        return list(authors)

    def article_titles(self):
        # Return list of strings of the titles of all articles written for that magazine
        from article import Article
        return [article.title for article in Article.all() if article.magazine == self]

    def contributing_authors(self):
        # Returns list of authors who have written more than 2 articles for the magazine
        from collections import Counter
        from article import Article
        
        author_counts = Counter(article.author for article in Article.all() if article.magazine == self)
        return [author for author, count in author_counts.items() if count > 2] 