"""optometria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from apps.home.views import Login, registro, logoutUsuario

urlpatterns = [
    path('home/', include(('apps.home.urls','home'))),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', Login.as_view(success_url="/home/"),  name = 'login'),
    path('registro/', registro,  name = 'registro'),
    path('logout/', login_required(logoutUsuario), name='logout'),
]
