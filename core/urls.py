from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('professions/', views.professions, name='professions'),
    path('professions/<slug:slug>/', views.profession_detail, name='profession_detail'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('api/groups/', views.api_groups),
    path('api/professions/', views.api_professions),
    path('api/news/', views.api_news),
]