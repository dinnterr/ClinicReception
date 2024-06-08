from django.urls import path
from . import views

urlpatterns = [
    path('', views.tickets_list, name='ticket_list'),
    path('new/', views.ticket_create, name='ticket_create'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('<int:pk>/edit/', views.ticket_edit, name='ticket_edit'),
    path('<int:pk>/delete/', views.ticket_delete, name='ticket_delete'),
]
