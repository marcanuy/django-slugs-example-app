import factory
from . import models


class ArticleUniqueSlugFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ArticleUniqueSlug

    title = factory.Faker("sentence", nb_words=10, variable_nb_words=True)

class ArticlePkAndSlugFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ArticleUniqueSlug

    title = factory.Faker("sentence", nb_words=10, variable_nb_words=True)

class Comparator(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comparator
