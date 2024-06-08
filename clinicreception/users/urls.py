from django.urls import path, include
from . import views

urlpatterns = [
    path('registrator', views.registrator, name='registrator_main'),
    path('registrator/tickets/', include('tickets.urls')),
    path('registrator/medcards/', include('medicalcards.registrator_medcards_urls')),
    path('medcontroller', views.medcontroller, name='medcontroller_main'),
    path('medcontroller/medcards/', include('medicalcards.medcontroller_medcards_urls')),
    path('admin', views.admin, name='admin_main'),
    path('admin/doctors/', include('doctors.urls')),
    path('admin/schedules/', include('schedules.urls')),
    path('statistic', views.statistic, name='statistic_main'),
    path('statistic/medcards/', include('medicalcards.statistic_medcards_urls')),
    path('statistic/doctors/', include('doctors.statistic_urls')),
    path('doctor', views.doctor, name='doctor_main'),
    path('doctor/tickets/', include('tickets.doctor_tickets_urls')),
    path('head', views.head, name='head_main'),
    path('head/receptionists/', include('receptionists.urls')),
    path('logout/', views.logout_view, name='logout'),

]
