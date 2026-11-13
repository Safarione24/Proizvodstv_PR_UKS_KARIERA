from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('professions/', views.professions, name='professions'),
    path('professions/<slug:slug>/', views.profession_detail, name='profession_detail'),
    path('self-prep/', views.self_prep, name='self_prep'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('toggle-vision/', views.toggle_vision, name='toggle_vision'), # <-- НОВЫЙ МАРШРУТ
    path('documents/', views.documents, name='documents'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('api/groups/', views.api_groups, name='api_groups'),
    path('api/professions/', views.api_professions, name='api_professions'),
    path('api/news/', views.api_news, name='api_news'),
]