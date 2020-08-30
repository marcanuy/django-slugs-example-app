import itertools

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ArticleMixin(object):
    title = models.CharField(max_length=settings.BLOG_TITLE_MAX_LENGTH)

class ArticleUniqueSlug(ArticleMixin, models.Model):
    title = models.CharField(max_length=settings.BLOG_TITLE_MAX_LENGTH)
    slug = models.SlugField(default="", editable=False, max_length=settings.BLOG_UNIQUE_SLUG_MAX_LENGTH)

    def get_absolute_url(self):
        kwargs = {"slug": self.slug}
        return reverse("articleunique-slug", kwargs=kwargs)

    def _generate_slug(self):
        max_length = settings.BLOG_UNIQUE_SLUG_MAX_LENGTH
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)[:max_length]
        for i in itertools.count(1):
            if not ArticleUniqueSlug.objects.filter(slug=slug_candidate).exists():
                break
            # Calculate the length of the candidate slug
            # considering separator and number length
            id_length = len(str(i)) + 1
            new_slug_text_part_length = len(slug_original) - id_length
            original_slug_with_id_length = len(slug_original) + id_length
            # truncate the candidate slug text if the whole candidate slug length
            # is greater than the Slug's database max_length
            candidate_slug_part = slug_original[:new_slug_text_part_length] if original_slug_with_id_length > max_length else slug_original
            slug_candidate = "{}-{}".format(candidate_slug_part, i)

        self.slug = slug_candidate

    def slug_length(self):
        return len(self.slug)

    def get_absolute_url(self):
        return reverse("articleunique-slug", args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)


class ArticlePkAndSlug(ArticleMixin, models.Model):
    title = models.CharField(max_length=settings.BLOG_TITLE_MAX_LENGTH)
    slug = models.SlugField(
        default="", editable=False, max_length=settings.BLOG_TITLE_MAX_LENGTH
    )
    def slug_length(self):
        """ Calculate length of strings like: id-slug
        """
        return len(str(self.id)) + 1 + len(self.slug)

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
