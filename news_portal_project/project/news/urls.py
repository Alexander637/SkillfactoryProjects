from django.urls import path
from .views import *

urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('articles/', ArticlesList.as_view(), name='article_list'),
    path('posts/', PostList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='new_detail'),
    path('articles/<int:pk>', PostDetail.as_view(), name='article_detail'),
    path('news/create/', PostCreate.as_view(), name='create_news'),
    path('articles/create/', PostCreate.as_view(), name='create_articles'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='edit_news'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='edit_article'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
