from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Permission


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super(LoginForm, self).__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
       
       self.fields['password'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
       
class NewUserForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name', 'last_name']
        labels = {
            'username' : 'Nombre de usuario', 'email': 'Correo electronico', 'password1': 'Contraseña', 'password2': 'Repetir contraseña', 'first_name': 'Nombres', 'last_name': 'Apellidos',
        }
        widgets = {
            'username' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su nombre de usuario'}
                ),
            'email' : forms.EmailInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su correo electrónico'}
                ),
            'password1' : forms.PasswordInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su contraseña'}
                ),
            'password2' : forms.PasswordInput(
                attrs = { 'class':'form-control', 'placeholder': 'Repita su contraseña'}
                ),
            'first_name' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese sus nombres', 'required': True, 'pattern':'[A-Za-z ]+'}
                ),
            'last_name' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese sus apellidos', 'required': True, 'pattern':'[A-Za-z ]+'}
                ),
        }