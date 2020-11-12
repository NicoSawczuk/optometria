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


# Create your views here.

def home (request):
    usr = request.user
    user = User.objects.get(id=usr.id)
    return render (request, 'home/home.html',{'user':user})


def indexPacientes (request):
    pacientes = Paciente.objects.all()
    return render (request, 'pacientes/index.html',{'pacientes':pacientes})


def createPaciente (request):
    medicos = Medico.objects.all()
    if request.method == 'GET':
        return render (request, 'pacientes/create.html',{'medicos':medicos})
    else:
        paciente = Paciente.objects.create(
            nombre = request.POST['nombre'],
            apellido = request.POST['apellido'],
            fecha_nac = request.POST['fecha_nac'],
            sexo = request.POST['sexo'],
            medico_id = Medico.objects.get(id=int(request.POST['medico'])).id,
        )
        paciente.save()
        messages.success(request, "Paciente agregado con exito")
        return redirect ('/home/pacientes/index')
    

def editarPaciente (request, pk):
    paciente = Paciente.objects.get(id=pk)
    medicoSelect = paciente.medico
    medicos = Medico.objects.all()
    if request.method == 'GET':
        return render (request, 'pacientes/edit.html',{'medicos':medicos, 'paciente':paciente, 'medicoSelect':medicoSelect})
    else:
        paciente = Paciente.objects.filter(id=request.POST['id']).update(
            nombre = request.POST['nombre'],
            apellido = request.POST['apellido'],
            fecha_nac = request.POST['fecha_nac'],
            sexo = request.POST['sexo'],
            medico_id = Medico.objects.get(id=int(request.POST['medico'])).id)
        messages.success(request, "Paciente modificado con exito")
        return redirect ('/home/pacientes/index')
    
def observacionesPaciente(request):
    observaciones = ObservacionPaciente.objects.filter(paciente_id=request.GET['id'])
    print(observaciones)
    
    data = serializers.serialize('json',observaciones,
                                     fields=('detalle', 'fecha'))
    
    return HttpResponse(data, content_type='application/json')

def createObservacionPaciente(request):
      
    observacion = ObservacionPaciente.objects.create(detalle=request.POST.get('detalle'), paciente_id=request.POST.get('id'))
    observacion.save()
    
    messages.success(request, "Observación agregada con éxito")
    return redirect ('/home/pacientes/index')


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