from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from .forms import ArticleForm

from blog.models import Comparator, ArticlePkAndSlug, ArticleUniqueSlug


class ComparatorListView(ListView):

    model = Comparator


class ComparatorFormView(FormView):
    template_name = "blog/comparator_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("article-list")

    def form_valid(self, form):
        new_title = form.cleaned_data.get("title")
        Comparator.generate(new_title=new_title)
        return super().form_valid(form)

class ArticlePkAndSlugDetailView(DetailView):
    model = ArticlePkAndSlug
    query_pk_and_slug = True
    template_name = "blog/article_detail.html"


class ArticleUniqueSlugDetailView(DetailView):
    model = ArticleUniqueSlug
    query_pk_and_slug = False
    template_name = "blog/article_detail.html"
