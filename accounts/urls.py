from django.urls import path 
from. import views

app_name='accounts'
    #config-> URLS
    #by Andrew, accounts --> Register/ Login/ Logout / Dashboard
    #path('accounts/',include('accounts.urls',namespace='accounts')),



urlspatterns = [ 
    path('login/',views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('dashboard',views.dashboard,name='dashboard'),

]