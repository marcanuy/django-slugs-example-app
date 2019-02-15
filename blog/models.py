from django.conf import settings
from django.db import models
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])

class ArticlePkAndSlug(models.Model):
    title = models.CharField(max_length=settings.BLOG_TITLE_MAX_LENGTH)
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
