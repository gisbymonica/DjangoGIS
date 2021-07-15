from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('streetmap', views.streetmap,name='streetmap'),
    path('buildings', views.buildings,name='buildings'),
    path('hospitals', views.hospitals,name='hospitals')
    ]
