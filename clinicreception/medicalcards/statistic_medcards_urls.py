from django.urls import path
from . import views

urlpatterns = [
    #path('', views.medcards_list, name='medcards_list'),
    path('', views.statistic, name='statistic_medcard'),

]
