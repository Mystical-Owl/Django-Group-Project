from django.urls import path
from .views import profile_view, profile_create, profile_update, profile_delete

urlpatterns = [
    path('', profile_view, name='profile_view'),
    path('create/', profile_create, name='profile_create'),
    path('update/', profile_update, name='profile_update'),
    path('delete/', profile_delete, name='profile_delete'),
]