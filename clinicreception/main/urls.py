from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
]
