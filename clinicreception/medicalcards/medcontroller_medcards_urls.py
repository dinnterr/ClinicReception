from django.urls import path
from . import views

urlpatterns = [
    path('', views.edit_status, name='edit_status_medcard'),
    path('deliver/', views.deliver_medcard, name='deliver_medcard'),
    path('remove/', views.remove_medcard, name='remove_medcard'),
    path('archive/', views.archive_medcard, name='archive_medcard'),
]
