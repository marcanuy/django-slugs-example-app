from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from blog.models import Article, ArticlePkAndSlug, ArticleUniqueSlug

class ArticleDetailView(DetailView):
    model = Article
    
    
class ArticleListView(ListView):

    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articlepkandslug_list'] = ArticlePkAndSlug.objects.all()
        context['articleuniqueslug_list'] = ArticleUniqueSlug.objects.all()

        return context

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title']

    success_url = reverse_lazy('article-list')

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        # create pk and slug model article
        ArticlePkAndSlug(title=title).save()
        # create unique slug article
        ArticleUniqueSlug(title=title).save()
        return super().form_valid(form)

class ArticlePkAndSlugDetailView(DetailView):
    model = ArticlePkAndSlug
    query_pk_and_slug = True
    template_name = 'blog/article_detail.html'

class ArticleUniqueSlugDetailView(DetailView):
    model = ArticlePkAndSlug
    query_pk_and_slug = False
    template_name = 'blog/article_detail.html'
