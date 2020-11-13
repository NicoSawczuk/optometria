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
    if(request.user.groups.filter(name='Profesional medico').exists()):
        turnos = Turno.objects.filter(medico_id=request.user.medico.id, activo=True)
        print(turnos)
        pacientes = []
        for turno in turnos:
            pacientes.append(turno.paciente)
    else:
        pacientes = Paciente.objects.all()
    return render (request, 'pacientes/index.html',{'pacientes':pacientes})


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
      
    observacion = ObservacionPaciente.objects.create(detalle=request.POST.get('detalle'), paciente_id=request.POST.get('id'))
    observacion.save()
    
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y-%m-%d")
    Turno.objects.filter(paciente_id=request.POST.get('id'), fecha=formatedDate).update(activo=False)
    
    messages.success(request, "Observación agregada con éxito")
    return redirect ('/home/pacientes/index')


def indexTurnos (request):
    turnos = Turno.objects.all()
    return render (request, 'turnos/index.html',{'turnos':turnos})

def createTurno (request):
    medicos = Medico.objects.all()
    pacientes = Paciente.objects.all()
    if request.method == 'GET':
        return render (request, 'turnos/create.html',{'medicos':medicos, 'pacientes':pacientes})
    else:
        if (Turno.objects.filter(paciente_id = request.POST.get('paciente'),fecha = request.POST.get('fecha'), activo=True).exists()):
            messages.error(request, 'El paciente ya tiene asignado un turno en el dia seleccionado')
            return redirect ('/home/turnos/index')
        else:
            turno = Turno.objects.create(
                paciente_id = request.POST.get('paciente'),
                medico_id = request.POST.get('medico'),
                fecha = request.POST.get('fecha'),
                detalle = request.POST.get('detalle'),
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