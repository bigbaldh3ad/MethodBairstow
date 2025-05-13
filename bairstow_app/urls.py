from django.urls import path
from . import views

urlpatterns = [
    path('', views.portada, name='portada'), 
    path('bairstow/', views.home, name='bairstow'),
    path('historial/', views.historial, name='historial'),
    
    path('api/bairstow/', views.BairstowListAPI.as_view(), name='api-list'),
    path('api/bairstow/new/', views.BairstowCreateAPI.as_view(), name='api-create'),
]