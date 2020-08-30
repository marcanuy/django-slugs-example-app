from django.conf import settings
from django.test import TestCase, override_settings

from .models import ArticleUniqueSlug, ArticlePkAndSlug
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

    @override_settings(BLOG_TITLE_MAX_LENGTH=10)
    @override_settings(BLOG_UNIQUE_SLUG_MAX_LENGTH=5)
    def test_slug_truncates_longer_titles(self):
        slug_max_length = settings.BLOG_UNIQUE_SLUG_MAX_LENGTH
        title = "a"*settings.BLOG_TITLE_MAX_LENGTH

        # generate one
        article = ArticleUniqueSlug.objects.create(title=title)
        self.assertEqual(len(article.slug), slug_max_length)
        

    @override_settings(BLOG_TITLE_MAX_LENGTH=10)
    @override_settings(BLOG_UNIQUE_SLUG_MAX_LENGTH=10)
    def test_title_max_length_slug_truncates(self):
        max_length = settings.BLOG_TITLE_MAX_LENGTH
        title = "a"*max_length
        expected_slug = "{}-1".format(title[:max_length-2])
        # generate one
        ArticleUniqueSlug.objects.create(title=title)
        # generate same title
        article = ArticleUniqueSlug.objects.create(title=title)

        self.assertEqual(len(article.title), len(article.slug))
        self.assertEqual(article.slug, expected_slug)

class ArticlePkAndSlugTests(TestCase):

    @override_settings(BLOG_TITLE_MAX_LENGTH=10)
    def test_slug_size_titles(self):
        max_length = settings.BLOG_TITLE_MAX_LENGTH
        title = "a"*max_length

        article = ArticlePkAndSlug.objects.create(title=title)

        self.assertEqual(len(article.slug), max_length)
        
