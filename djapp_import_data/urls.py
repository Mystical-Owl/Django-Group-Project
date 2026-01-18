## must add this file for every new django app with endpoints

from django.urls import path
from . import views

app_name = 'app_import_data'

urlpatterns = [
    path('', views.func_import_index, name='djep_import_index'),
    path('import_default_data/', views.func_import_default_data, name='djep_import_default_data'),
    path('delete_default_data/', views.func_delete_default_data, name='djep_delete_default_data'),
]
