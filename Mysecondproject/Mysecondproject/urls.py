"""
URL configuration for Mysecondproject project.

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
from django.urls import path,include

from Firstapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('neth/',views.Nethaji),
    path('',views.Webpage),
    path('login/',views.Loginpage,name="login"),
    path('support/',views.Supportpage,name="support"),
    path('second/',include("Secondapp.urls")),
    path('model/',include("Modelapp.url")),
    path('alertapp/',include("Alertapp.url")),
    path('CRUD/',include("CRUDapp.url")),
    path('api-auth/', include('rest_framework.urls')),
    path('rest/',include('Restapp.url')),
    path('practice/',include('Practice.url')),
    path('IT/',include('ITSupport.url')),
    path('Test/',include('Testapp.url')),
    path('Mohan/',include('Mohanapp.url')),
    path('API/',include('VEapp.url')),
    path('restau/',include('restaurant.url'))
]
