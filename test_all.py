import pytest
from author import Author
from magazine import Magazine
from article import Article

def test_author_properties():
    author = Author("John Smith")
    assert author.name == "John Smith"
    assert author.articles == []

def test_magazine_properties():
    magazine = Magazine("Tech Weekly", "Technology")
    assert magazine.name == "Tech Weekly"
    assert magazine.category == "Technology"

def test_article_creation():
    author = Author("Jane Doe")
    magazine = Magazine("Science Monthly", "Science")
    article = author.add_article(magazine, "The Future of AI")
    
    assert article.title == "The Future of AI"
    assert article.author == author
    assert article.magazine == magazine
    assert article in author.articles

def test_author_topic_areas():
    author = Author("Bob Wilson")
    tech_mag = Magazine("Tech Review", "Technology")
    science_mag = Magazine("Science Today", "Science")
    
    author.add_article(tech_mag, "Python Tips")
    author.add_article(science_mag, "Quantum Computing")
    
    topic_areas = author.topic_areas()
    assert "Technology" in topic_areas
    assert "Science" in topic_areas
    assert len(topic_areas) == 2

def test_author_magazines():
    author = Author("Alice Brown")
    magazine1 = Magazine("Food Weekly", "Cooking")
    magazine2 = Magazine("Food Weekly", "Cooking")  # Same magazine
    
    author.add_article(magazine1, "Pasta Recipe")
    author.add_article(magazine2, "Pizza Recipe")
    
    magazines = author.magazines()
    assert len(magazines) == 1  # Should only count unique magazines

def test_magazine_contributors():
    magazine = Magazine("Sports Weekly", "Sports")
    author1 = Author("Tom Jones")
    author2 = Author("Sarah Wilson")
    
    author1.add_article(magazine, "Football Analysis")
    author2.add_article(magazine, "Tennis Update")
    
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert author1 in contributors
    assert author2 in contributors

def test_magazine_article_titles():
    magazine = Magazine("Art Monthly", "Art")
    author = Author("Pablo Smith")
    
    author.add_article(magazine, "Modern Art Trends")
    author.add_article(magazine, "Classical Paintings")
    
    titles = magazine.article_titles()
    assert "Modern Art Trends" in titles
    assert "Classical Paintings" in titles
    assert len(titles) == 2

def test_contributing_authors():
    magazine = Magazine("Daily News", "News")
    author = Author("Mike Johnson")
    
    # Add 3 articles
    author.add_article(magazine, "Article 1")
    author.add_article(magazine, "Article 2")
    author.add_article(magazine, "Article 3")
    
    contributing_authors = magazine.contributing_authors()
    assert author in contributing_authors 