from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Medico(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    apellido = models.CharField(max_length = 60, blank = False, null = True)
    fecha_nac = models.CharField(blank = False, null = True,max_length = 10,)
    sexo = models.CharField(max_length = 1, blank = False, null = True)
    estado = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    class Meta:
        verbose_name = 'Medico'
        verbose_name_plural = 'Medico'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    
class Paciente(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    apellido = models.CharField(max_length = 60, blank = False, null = True)
    fecha_nac = models.CharField(blank = False, null = True,max_length = 10,)
    sexo = models.CharField(max_length = 1, blank = False, null = True)
    estado = models.BooleanField(default=True)
    medico = models.ForeignKey(Medico, verbose_name="Medico", on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre