## must add this file for every new django app

from django.urls import path
from . import views

# same as namespace in config/urls.py
app_name = 'app_accounts'

### urlpatterns is a hook from django
urlpatterns = [
    path('login/', views.func_login, name='djep_login'),
    path('logout/', views.func_logout, name='djep_logout'),
    path('register/', views.func_register, name='djep_register'),
    path('dashboard/', views.func_dashboard, name='djep_dashboard'),
]
