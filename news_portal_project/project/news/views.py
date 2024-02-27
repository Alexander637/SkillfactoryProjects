from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    queryset = Post.objects.filter(categoryType="NW").order_by('-dateCreation')
    template_name = 'news.html'
    context_object_name = 'news'


class NewDetail(DetailView):
    queryset = Post.objects.filter(categoryType="NW")
    template_name = 'new.html'
    context_object_name = 'new'


class ArticlesList(ListView):
    queryset = Post.objects.filter(categoryType="AR").order_by('-dateCreation')
    template_name = 'articles.html'
    context_object_name = 'articles'


class ArticleDetail(DetailView):
    queryset = Post.objects.filter(categoryType="AR")
    template_name = 'article.html'
    context_object_name = 'article'
