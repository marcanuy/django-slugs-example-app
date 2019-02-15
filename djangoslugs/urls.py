"""djangoslugs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from blog.views import (ArticleDetailView, ArticleListView,
                        ArticleCreateView, ArticlePkAndSlugDetailView,
                        ArticleUniqueSlugDetailView)

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('blog/create', ArticleCreateView.as_view(), name='article-create'),
    path('blog/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('blog/<int:pk>-<str:slug>/', ArticlePkAndSlugDetailView.as_view() , name='article-pk-slug-detail'),
    path('blog/<str:slug>', ArticleUniqueSlugDetailView.as_view(), name='articleunique-slug')
]
