## must add this file for every new django app with endpoints

from django.urls import path
from . import views

app_name = 'app_import_data'

urlpatterns = [
    path('', views.func_import_index, name='djep_import_index'),
    path(
        'urlep_import_default_questionaire_data/',
        views.func_import_default_questionaire_data,
        name='djep_import_default_questionaire_data'
    ),
    path(
        'urlep_update_questionaires_min_max_score/',
        views.func_update_questionaires_min_max_score,
        name='djep_update_questionaires_min_max_score'
    ),
    path(
        'urlep_delete_default_questionaire_data/',
        views.func_delete_default_questionaire_data,
        name='djep_delete_default_questionaire_data'
    ),
    path(
        'urlep_import_default_investment_datas/',
        views.func_import_default_investment_datas,
        name='djep_import_default_investment_datas'
    ),
    path(
        'urlep_delete_default_investment_datas/',
        views.func_delete_default_investment_datas,
        name='djep_delete_default_investment_datas'
    ),
]
