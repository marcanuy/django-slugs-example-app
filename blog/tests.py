from django.test import TestCase

from .factories import ArticleUniqueSlugFactory

class ArticleUniqueSlugTests(TestCase):
    
    def test_generates_slug(self):
        article = ArticleUniqueSlugFactory.create()

        self.assertIsNotNone(article.slug)

    def test_not_generates_slug_if_updating(self):
        article = ArticleUniqueSlugFactory.create()
        original_slug = article.slug
        article.title = "foo"

        article.save()

        self.assertEqual(article.slug, original_slug)
