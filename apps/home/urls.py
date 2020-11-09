from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import home, indexPacientes

urlpatterns = [
    path('', home, name = 'index'),
    path('pacientes/index', login_required(indexPacientes), name = 'indexPacientes'),
]