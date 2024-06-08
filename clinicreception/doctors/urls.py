from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctors_list, name='doctor_list'),
    path('new/', views.doctor_create, name='doctor_create'),
    #path('<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('select/', views.select_doctor_view, name='select_doctor'),
    path('edit/<int:doctor_id>/', views.edit_doctor_view, name='doctor_edit'),
    path('delete/', views.doctor_delete, name='doctor_delete'),
]
