from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from blog.models import Article

class ArticleDetailView(DetailView):

    model = Article

class ArticleListView(ListView):

    model = Article

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title']

