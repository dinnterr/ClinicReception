from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedules_list, name='schedules_list'),
    path('management/', views.schedules_management, name='schedules_management'),
    path('select_doctor/', views.select_doctor_view, name='select_doctor'),
    path('<int:doctor_id>/', views.get_doctor_schedule_view, name='doctor_schedule'),

    #path('edit/<int:schedule_id>/', views.edit_schedules, name='schedules_edit'),
    #path('delete/', views.doctor_delete, name='doctor_delete'),
]
