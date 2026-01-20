## must add this file for every new django app with endpoints

from django.urls import path
from . import views

app_name = 'questionaires'

urlpatterns = [
    path('', views.index, name='index'),
    path('save_uqa/', views.save_uqa, name='save_uqa'),
    path('<str:questionaire_type>/', views.questionaire, name='questionaire'),
]
