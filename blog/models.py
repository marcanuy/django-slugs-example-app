import itertools

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# class ArticleMixin(object):
#     title = models.CharField(max_length=settings.BLOG_TITLE_MAX_LENGTH)

#class ArticleUniqueSlug(ArticleMixin, models.Model):
class ArticleUniqueSlug(models.Model):
    title = models.CharField(max_length=settings.BLOG_TITLE_MAX_LENGTH)
    slug = models.SlugField(default="", editable=False, max_length=100)  # random length

    def get_absolute_url(self):
        kwargs = {"slug": self.slug}
        return reverse("articleunique-slug", kwargs=kwargs)

    def _generate_slug(self):
        max_length = self._meta.get_field("slug").max_length
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not ArticleUniqueSlug.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = "{}-{}".format(slug_original, i)

        self.slug = slug_candidate

    def get_absolute_url(self):
        return reverse("articleunique-slug", args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)


#class ArticlePkAndSlug(ArticleMixin, models.Model):
class ArticlePkAndSlug(models.Model):
    title = models.CharField(max_length=settings.BLOG_TITLE_MAX_LENGTH)
    slug = models.SlugField(
        default="", editable=False, max_length=settings.BLOG_TITLE_MAX_LENGTH
    )

    def get_absolute_url(self):
        kwargs = {"pk": self.id, "slug": self.slug}
        return reverse("article-pk-slug-detail", kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Comparator(models.Model):
    article_pk_and_slug = models.OneToOneField('ArticlePkAndSlug', on_delete=models.CASCADE)
    article_unique_slug = models.OneToOneField('ArticleUniqueSlug', on_delete=models.CASCADE)

    @classmethod
    def generate(cls, new_title):
        pk_and_slug=ArticlePkAndSlug.objects.create(title=new_title)
        unique_slug=ArticleUniqueSlug.objects.create(title=new_title)
        comparator = cls.objects.create(
            article_pk_and_slug = pk_and_slug,
            article_unique_slug = unique_slug,
        )
        return comparator
