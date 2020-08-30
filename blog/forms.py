from django.conf import settings
from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=settings.BLOG_TITLE_MAX_LENGTH)
