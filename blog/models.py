import itertools

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Article(models.Model):
    title = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])

class ArticleUniqueSlug(Article):

    slug = models.SlugField(
        default='',
        editable=False,
        max_length=100, #random length
    )

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse('articleunique-slug', kwargs=kwargs)


    def save(self, *args, **kwargs):
        max_length = self._meta.get_field('slug').max_length
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not ArticleUniqueSlug.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate
        super().save(*args, **kwargs)


class ArticlePkAndSlug(models.Model):
    title = models.CharField(
        max_length=settings.BLOG_TITLE_MAX_LENGTH
    )
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=settings.BLOG_TITLE_MAX_LENGTH,
    )

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('article-pk-slug-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


