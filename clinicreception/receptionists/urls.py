from django.urls import path
from . import views

urlpatterns = [
    path('', views.receptionists_list, name='receptionists_list'),
    path('create/', views.receptionist_create, name='receptionist_create'),
    path('delete/', views.receptionist_delete, name='receptionist_delete'),
]
