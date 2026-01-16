## must add this file for every new django app with endpoints

from django.urls import path
from . import views

app_name = 'app_questionaire_answers'

urlpatterns = [
    path('import_default_data/', views.func_import_default_data, name='djep_import_default_data'),
]
