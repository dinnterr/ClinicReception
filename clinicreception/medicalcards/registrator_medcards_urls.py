from django.urls import path
from . import views

urlpatterns = [
    path('', views.medcards_list, name='medcards_list'),
    path('new/', views.medcard_create, name='medcard_create'),
    path('<int:pk>/', views.medcard_detail, name='medcard_detail'),
    path('<int:pk>/edit/', views.medcard_edit, name='medcard_edit'),
    path('<int:pk>/delete/', views.medcard_delete, name='medcard_delete'),
    path('search/', views.search_medical_card, name='search_medical_card'),
]
