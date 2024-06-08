from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_statistic, name='statistic_doc'),
]
