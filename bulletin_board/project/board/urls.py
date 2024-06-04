from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('advertisements/', AdvertisementList.as_view(), name='advertisements'),
    path('advertisement/<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('advertisement/create/', AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('advertisement/<int:pk>/update/', AdvertisementUpdateView.as_view(), name='advertisement_update'),
    path('advertisement/<int:pk>/delete/', AdvertisementDeleteView.as_view(), name='advertisement_delete'),
    path('advertisement/<int:pk>/respond/', ResponseCreateView.as_view(), name='response_create'),
    path('response/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response_delete'),
]
