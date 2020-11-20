from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import home, indexPacientes, createPaciente, editPaciente, observacionesPaciente, createObservacionPaciente, indexTurnos, createTurno, editTurno, deleteTurno, indexProductos, createProducto, editProducto, deleteProducto, indexPedidos, createPedido, editPedido, deletePedido

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

    #Productos
    path('productos/index', login_required(indexProductos), name = 'indexProductos'),
    path('productos/create', login_required(createProducto), name = 'createProducto'),
    path('productos/edit/<int:pk>', login_required(editProducto), name='editProducto'),
    path('productos/delete/<int:pk>', login_required(deleteProducto), name='deleteProducto'),
    
    #Pedidos
    path('pedidos/index', login_required(indexPedidos), name = 'indexPedidos'),
    path('pedidos/create', login_required(createPedido), name = 'createPedido'),
    path('pedidos/edit/<int:pk>', login_required(editPedido), name='editPedido'),
    path('pedidos/delete/<int:pk>', login_required(deletePedido), name='deletePedido'),
]