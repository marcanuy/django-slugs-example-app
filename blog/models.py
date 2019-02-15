from django.db import models
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])
