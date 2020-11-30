from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib.auth.models import Group
from .forms import LoginForm, NewUserForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User, Permission
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime


# Create your views here.

def home (request):
    usr = request.user
    user = User.objects.get(id=usr.id)
    return render (request, 'home/home.html',{'user':user})


def indexPacientes (request):
    #Si es medico
    estados = EstadoTurno.objects.all()
    if(request.user.groups.filter(name='Profesional medico').exists()):
        turnos = Turno.objects.filter(medico_id=request.user.medico.id)
        print(turnos)
        pacientes = []
        for turno in turnos:
            if not(turno.paciente in pacientes):
                pacientes.append(turno.paciente)
    else:
        pacientes = Paciente.objects.all()
    return render (request, 'pacientes/index.html',{'pacientes':pacientes, 'estados':estados})


def createPaciente (request):
    if request.method == 'GET':
        return render (request, 'pacientes/create.html')
    else:
        paciente = Paciente.objects.create(
            nombre = request.POST['nombre'],
            apellido = request.POST['apellido'],
            fecha_nac = request.POST['fecha_nac'],
            sexo = request.POST['sexo'],
        )
        paciente.save()
        messages.success(request, "Paciente agregado con exito")
        return redirect ('/home/pacientes/index')
    

def editPaciente (request, pk):
    paciente = Paciente.objects.get(id=pk)
    if request.method == 'GET':
        return render (request, 'pacientes/edit.html',{ 'paciente':paciente})
    else:
        paciente = Paciente.objects.filter(id=request.POST['id']).update(
            nombre = request.POST['nombre'],
            apellido = request.POST['apellido'],
            fecha_nac = request.POST['fecha_nac'],
            sexo = request.POST['sexo'])
        messages.success(request, "Paciente modificado con exito")
        return redirect ('/home/pacientes/index')
    
def observacionesPaciente(request):
    observaciones = ObservacionPaciente.objects.filter(paciente_id=request.GET['id']).order_by('-id')
    print(observaciones)
    
    data = serializers.serialize('json',observaciones,
                                     fields=('detalle', 'fecha'))
    
    return HttpResponse(data, content_type='application/json')

def createObservacionPaciente(request):
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y-%m-%d")
    if Turno.objects.filter(paciente_id=request.POST.get('id'), fecha=formatedDate).exists():
        observacion = ObservacionPaciente.objects.create(detalle=request.POST.get('detalle'), paciente_id=request.POST.get('id'))
        observacion.save()
        
        Turno.objects.filter(paciente_id=request.POST.get('id'), fecha=formatedDate).update(estado=EstadoTurno.objects.get(nombre='Atendido'))
    
        messages.success(request, "Observación agregada con éxito")
        return redirect ('/home/turnos/index')
    else:
        messages.error(request, "No puede agregar observaciones a turnos que no sean del dia de hoy")
        return redirect ('/home/turnos/index')

def registrarFalta (request,pk):
    turno = Turno.objects.get(id=pk)
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y-%m-%d")
    if turno.fecha <= formatedDate:
        Turno.objects.filter(id=pk).update(estado=EstadoTurno.objects.get(nombre='No asistió'))
        
        messages.success(request, "Falta registrada con éxito")
        return redirect ('/home/turnos/index')
    else:
        messages.error(request, "No puedes registrar una falta antes del dia")
        return redirect ('/home/turnos/index')


def indexTurnos (request):
    if(request.user.groups.filter(name='Profesional medico').exists()):
        turnos = Turno.objects.filter(medico_id=request.user.medico.id)
    else:
        turnos = Turno.objects.all()
    pacientes = Paciente.objects.all()
    estados = EstadoTurno.objects.all()
    return render (request, 'turnos/index.html',{'turnos':turnos, 'pacientes': pacientes, 'estados': estados})

def createTurno (request):
    medicos = Medico.objects.all()
    pacientes = Paciente.objects.all()
    if request.method == 'GET':
        return render (request, 'turnos/create.html',{'medicos':medicos, 'pacientes':pacientes})
    else:
        if (Turno.objects.filter(paciente_id = request.POST.get('paciente'),fecha = request.POST.get('fecha'), estado=EstadoTurno.objects.get(nombre='Sin atender')).exists()):
            messages.error(request, 'El paciente ya tiene asignado un turno en el dia seleccionado')
            return redirect ('/home/turnos/index')
        else:
            turno = Turno.objects.create(
                paciente_id = request.POST.get('paciente'),
                medico_id = request.POST.get('medico'),
                fecha = request.POST.get('fecha'),
                detalle = request.POST.get('detalle'),
                estado=EstadoTurno.objects.get(nombre='Sin atender'),
            )
            turno.save()
            messages.success(request, "Turno agregado con exito")
            return redirect ('/home/turnos/index')


def editTurno (request, pk):
    turno = Turno.objects.get(id=pk)
    medicos = Medico.objects.all()
    pacientes = Paciente.objects.all()
    if request.method == 'GET':
        return render (request, 'turnos/edit.html',{'turno':turno, 'medicos':medicos, 'pacientes':pacientes})
    else:
        turno = Turno.objects.filter(id=request.POST['id']).update(
            medico_id = request.POST.get('medico'),
            fecha = request.POST.get('fecha'),
            detalle = request.POST.get('detalle'),
        )
        messages.success(request, "Turno modificado con exito")
        return redirect ('/home/turnos/index')
    
def deleteTurno(request,pk):
    Turno.objects.get(id=pk).delete()
    messages.success(request, "Turno eliminado con exito")
    return redirect ('/home/turnos/index')

def indexProductos (request):
    productos = Producto.objects.all()
    return render (request, 'productos/index.html',{'productos':productos})

def createProducto (request):
    if request.method == 'GET':
        caracteristicasProducto = CaracteristicaProducto.objects.all()
        return render (request, 'productos/create.html', {'caracteristicasProducto':caracteristicasProducto})
    else:
        caracteristicaProducto = CaracteristicaProducto.objects.get(id=request.POST['caracteristicaProducto'])
        valorCaracteristicaProducto = ValorCaracteristicaProducto.objects.get(id=request.POST['valorCaracteristicaProducto'])
        producto = Producto.objects.create(
            nombre = request.POST['nombre'],
            descripcion = request.POST['descripcion'],
            caracteristicaProducto = caracteristicaProducto,
            valorCaracteristicaProducto = valorCaracteristicaProducto,
            precio = request.POST.get('precio'),
        )
        producto.save()
        messages.success(request, "Producto agregado con exito")
        return redirect ('/home/productos/index')

def editProducto (request, pk):
    producto = Producto.objects.get(id=pk)
    caracteristicasProducto = CaracteristicaProducto.objects.all()
    valorCaracteristicasProducto = ValorCaracteristicaProducto.objects.filter(caracteristicaproducto=producto.caracteristicaProducto.id)
    if request.method == 'GET':
        return render (request, 'productos/edit.html',{'producto':producto, 'caracteristicasProducto':caracteristicasProducto, 'valorCaracteristicasProducto':valorCaracteristicasProducto})
    else:
        caracteristicaProducto = CaracteristicaProducto.objects.get(id=request.POST['caracteristicaProducto'])
        valorCaracteristicaProducto = ValorCaracteristicaProducto.objects.get(id=request.POST['valorCaracteristicaProducto'])
        producto = Producto.objects.filter(id=request.POST['id']).update(
            nombre = request.POST['nombre'],
            descripcion = request.POST['descripcion'],
            caracteristicaProducto = caracteristicaProducto,
            valorCaracteristicaProducto = valorCaracteristicaProducto,
            precio = request.POST.get('precio'),
        )
        messages.success(request, "Producto actualizado con exito")
        return redirect ('/home/productos/index')

def deleteProducto (request, pk):
    Producto.objects.get(id=pk).delete()
    messages.success(request, "Producto eliminado con exito")
    return redirect ('/home/productos/index')

def getValores (request):
    valores = ValorCaracteristicaProducto.objects.filter(caracteristicaproducto=request.GET['id'])
    data = serializers.serialize('json', valores, fields=('id','valor'))
    return HttpResponse(data, content_type='application/json')




def indexPedidos (request):
    pedidos = Pedido.objects.all()
    estados = EstadoPedido.objects.all()
    return render (request, 'pedidos/index.html',{'pedidos':pedidos, 'estados': estados})

def createPedido (request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        tiposDePago = TipoDePago.objects.all()
        pacientes = Paciente.objects.all()
        
        return render (request, 'pedidos/create.html',{'productos':productos, 'tiposDePago': tiposDePago, 'pacientes': pacientes})
    else:
        
        pedido = Pedido.objects.create(
            paciente = Paciente.objects.get(id=request.POST.get('paciente')),
            subtotal = request.POST.get('subtotal'),
            estado = EstadoPedido.objects.get(nombre='Pendiente'),
            tipoDePago = TipoDePago.objects.get(id=request.POST.get('tipo_pago')),
            user= User.objects.get(id=request.user.id)
        )
        productos = request.POST.getlist('productos')
        for producto in productos:
            pedido.producto.add(Producto.objects.get(id=producto))
        pedido.save()
        messages.success(request, "Pedido agregado con exito")
        return redirect ('/home/pedidos/index')
    
def editPedido (request, pk):
    pedido = Pedido.objects.get(id=pk)
    productos = Producto.objects.all()
    tiposDePago = TipoDePago.objects.all()
    pacientes = Paciente.objects.all()
    if request.method == 'GET':
        return render (request, 'pedidos/edit.html',{'pedido':pedido, 'productos':productos, 'pacientes':pacientes, 'tiposDePago':tiposDePago})
    else:
        pedido = Pedido.objects.filter(id=pk).update(
                paciente = Paciente.objects.get(id=request.POST.get('paciente')),
                subtotal = request.POST.get('subtotal'),
                tipoDePago = TipoDePago.objects.get(id=request.POST.get('tipo_pago'))
            )
        pedido = Pedido.objects.get(id=pk)
        productos = request.POST.getlist('productos')
        print(pedido.getProductos())
        for producto in pedido.getProductos():
            pedido.producto.remove(producto)
        
        for producto in productos:
            pedido.producto.add(Producto.objects.get(id=producto))
        pedido.save()
        messages.success(request, "Pedido modificado con exito")
        return redirect ('/home/pedidos/index')

def deletePedido (request, pk):
    Pedido.objects.get(id=pk).delete()
    messages.success(request, "Pedido eliminado con exito")
    return redirect ('/home/pedidos/index')

def cambiarEstadoPedido (request):
    estado = EstadoPedido.objects.get(id=request.POST.get('estado'))
    if (estado.nombre == 'Finalizado'):
        myDate = datetime.now()
        formatedDate = myDate.strftime("%Y-%m-%d")
        Pedido.objects.filter(id=request.POST.get('pedido')).update(estado_id=request.POST.get('estado'), fecha_finalizado=formatedDate)
    else:
        Pedido.objects.filter(id=request.POST.get('pedido')).update(estado_id=request.POST.get('estado'))
    
    messages.success(request, "Estado del pedido modificado con exito")
    return redirect ('/home/pedidos/index')
    

def getValoresCaracteristica (request):
    print(request.GET['id'])
    caracteristica = CaracteristicaProducto.objects.get(id = request.GET['id']).valor.all()
    print(caracteristica)
    data = serializers.serialize('json',caracteristica, fields=('id', 'valor'))
    return HttpResponse(data, content_type='application/json')




def indexVentas(request):
    ventas = Pedido.objects.filter(estado__nombre='Finalizado')
    vendedores = User.objects.filter(groups__name='Ventas')
    tiposPago = TipoDePago.objects.all()
    return render (request, 'ventas/index.html',{'ventas':ventas, 'tiposPago':tiposPago, 'vendedores':vendedores})

class Login(FormView):
    template_name='login.html'
    form_class = LoginForm
    succes_url = reverse_lazy('/home')
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    
    def dispath(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url)
        else:
            return super(Login,self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        dj_login(self.request,form.get_user())
        return super(Login,self).form_valid(form)
    
def registro(request):               
    if request.method == 'POST':
        peticion = request.POST.copy()
        form = NewUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            dj_login(request, user)
            user.save()
            #Le asignamos el rol
            nombreGrupo = peticion.pop('rol')
            grupo = Group.objects.get(name=nombreGrupo[0]) 
            grupo.user_set.add(user)
            
            #Creamos la instancia de medico si lo es
            if (str(nombreGrupo[0]) == "Profesional medico"):
                medico = Medico.objects.create(nombre=request.POST.get('first_name'),apellido=request.POST.get('last_name'),fecha_nac=request.POST.get('fecha_nac'),sexo=request.POST.get('sexo'), user_id=user.id)
                medico.save()
            return redirect ('/home')
        else:
            error = form.errors
                
            return render(request, 'registro.html', context={'form': form, 'error':error})            

    form = NewUserForm
    return render(request, 'registro.html', context={'form': form})


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/login/')