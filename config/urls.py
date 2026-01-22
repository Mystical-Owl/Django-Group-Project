"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
#from django.conf.urls.static import static
# from django.conf import settings # Import settings

### add import for django debug toolbar
from config.settings import IS_DEVELOPMENT
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    # by Andrew, pages
    # modified by Franco
    path('', include('pages.urls', namespace='pages')),

    # by Andrew, contacts -> Message Boxed 
   # path('contacts/',include('contacts.urls',namespace='contacts')),

    #by Andrew, accounts --> Register/ Login/ Logout / Dashboard
    path('accounts/',include('accounts.urls',namespace='accounts')),

    # by Howard, becasue profiles.urls.py was created
    path('profile/', include('profiles.urls')),
    # by George
    path('questionaires/', include('questionaires.urls', namespace='questionaires')),
    path('admin/', admin.site.urls),
    # by George
    # only need to import data with new a database
    path('import_data/', include('djapp_import_data.urls', namespace='app_import_data')),
]


if IS_DEVELOPMENT:
    urlpatterns += debug_toolbar_urls()

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]


### change title words in django admin pages
admin.site.site_header = "WealthHub Administration"
admin.site.site_title = "WealthHub Admin Portal"
admin.site.index_title = "Welcome to WealthHub Portal"

