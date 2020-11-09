from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login as dj_login, logout, authenticate
from .forms import LoginForm, NewUserForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User, Permission
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

def home (request):
    return render (request, 'home/home.html')



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
        form = NewUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            dj_login(request, user)
            #permission = Permission.objects.get(name='Can view Rutina')
            #user.user_permissions.add(permission)
            user.save()
            return redirect ('/home')
        else:
            error = form.errors
                
            return render(request, 'registro.html', context={'form': form, 'error':error})            

    form = NewUserForm
    return render(request, 'registro.html', context={'form': form})


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/login/')