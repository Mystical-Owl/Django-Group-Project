## must add this file for every new django app with endpoints

from django.urls import path
from . import views

app_name = 'user_investments'

urlpatterns = [
    path('', views.index, name='index'),
    path('show/', views.show, name='show'),
    path('choices/', views.choices, name='choices'),
    path('save/', views.save, name='save'),
]
