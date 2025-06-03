class Author:
    def __init__(self, name):
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @property
    def articles(self):
        return self._articles

    def add_article(self, magazine, title):
        from article import Article
        article = Article(self, magazine, title)
        self._articles.append(article)
        return article

    def topic_areas(self):
        # Return unique list of categories from all magazines this author has published in
        categories = set()
        for article in self.articles:
            if article.magazine:
                categories.add(article.magazine.category)
        return list(categories)

    def magazines(self):
        # Return unique list of Magazine instances this author has published in
        return list(set(article.magazine for article in self.articles if article.magazine))

    def articles_by_magazine(self, magazine):
        # Return list of Article instances written by this author for a magazine
        return [article for article in self.articles if article.magazine == magazine] 