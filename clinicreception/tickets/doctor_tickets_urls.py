from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_ticket_list, name='appointment_ticket_list'),
    path('edit_status/', views.edit_ticket_status, name='ticket_for_doctor'),

]
