from django.urls import path
from .views import NewsList, ArticlesList, NewDetail, ArticleDetail

urlpatterns = [
    path('news/', NewsList.as_view()),
    path('articles/', ArticlesList.as_view()),
    path('news/<int:pk>', NewDetail.as_view(), name='new_detail'),
    path('articles/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
]
