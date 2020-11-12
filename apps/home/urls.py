from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import home, indexPacientes, createPaciente, editarPaciente, observacionesPaciente, createObservacionPaciente

urlpatterns = [
    path('', login_required(home), name = 'index'),
    path('pacientes/index', login_required(indexPacientes), name = 'indexPacientes'),
    path('pacientes/create', login_required(createPaciente), name = 'createPaciente'),
    path('pacientes/edit/<int:pk>', login_required(editarPaciente), name='editPaciente'),
    path('pacientes/observaciones', login_required(observacionesPaciente), name='observacionesPaciente'),
    path('pacientes/observaciones/create', login_required(createObservacionPaciente), name='createObservacionPaciente'),
]