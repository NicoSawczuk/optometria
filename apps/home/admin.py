from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(ObservacionPaciente)
admin.site.register(EstadoTurno)
admin.site.register(Turno)
admin.site.register(TipoDePago)
admin.site.register(EstadoPedido)
admin.site.register(ValorCaracteristicaProducto)
admin.site.register(CaracteristicaProducto)
admin.site.register(Producto)
admin.site.register(Pedido)