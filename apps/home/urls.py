from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import home, indexPacientes, createPaciente, editPaciente, observacionesPaciente, createObservacionPaciente, indexTurnos, createTurno, editTurno, deleteTurno

urlpatterns = [
    path('', login_required(home), name = 'index'),
    
    #Pacientes
    path('pacientes/index', login_required(indexPacientes), name = 'indexPacientes'),
    path('pacientes/create', login_required(createPaciente), name = 'createPaciente'),
    path('pacientes/edit/<int:pk>', login_required(editPaciente), name='editPaciente'),
    path('pacientes/observaciones', login_required(observacionesPaciente), name='observacionesPaciente'),
    path('pacientes/observaciones/create', login_required(createObservacionPaciente), name='createObservacionPaciente'),
    
    #Turnos
    path('turnos/index', login_required(indexTurnos), name = 'indexTurnos'),
    path('turnos/create', login_required(createTurno), name = 'createTurno'),
    path('turnos/edit/<int:pk>', login_required(editTurno), name='editTurno'),
    path('turnos/delete/<int:pk>', login_required(deleteTurno), name='deleteTurno'),
]