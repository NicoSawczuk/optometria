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
        return self.nombre + ' ' + self.apellido
    
    
class Paciente(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    apellido = models.CharField(max_length = 60, blank = False, null = True)
    fecha_nac = models.CharField(blank = False, null = True,max_length = 10,)
    sexo = models.CharField(max_length = 1, blank = False, null = True)
    estado = models.BooleanField(default=True)
    #medico = models.ForeignKey(Medico, verbose_name="Medico", on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class ObservacionPaciente(models.Model):
    id = models.AutoField(primary_key = True)
    detalle = models.TextField(blank = False, null = True)
    paciente = models.ForeignKey(Paciente, verbose_name="Paciente", on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'ObservacionPaciente'
        verbose_name_plural = 'ObservacionesPacientes'
        ordering = ['fecha']
    
    def __str__(self):
        return 'Observacion '+ self.paciente.nombre +' '+ self.paciente.apellido
    
class Turno(models.Model):
    id = models.AutoField(primary_key = True)
    paciente = models.ForeignKey(Paciente, verbose_name="Paciente", on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, verbose_name="Medico", on_delete=models.CASCADE)
    fecha = models.CharField(blank = False, null = True,max_length = 10)
    detalle = models.TextField(blank = False, null = True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['id']
    
    def __str__(self):
        return 'Turno '+ self.paciente.nombre +' '+ self.paciente.apellido
    
class TipoDePago(models.Model):
    id = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 60, blank = False, null = True)

    class Meta:
        verbose_name = 'TipoDePago'
        verbose_name_plural = 'TiposDePagos'
        ordering = ['descripcion']
    
    def __str__(self):
        return self.descripcion
    
class EstadoPedido(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    descripcion = models.CharField(max_length = 60, blank = False, null = True)
    colorEtiqueta = models.CharField(max_length = 7, blank = False, null = True)

    class Meta:
        verbose_name = 'EstadoPedido'
        verbose_name_plural = 'EstadosPedidos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class ValorCaracteristicaProducto(models.Model):
    id = models.AutoField(primary_key = True)
    valor = models.CharField(max_length = 60, blank = False, null = True)

    class Meta:
        verbose_name = 'ValorCaracteristicaProducto'
        verbose_name_plural = 'ValorCaracteristicaProductos'
        ordering = ['valor']
    
    def __str__(self):
        return self.valor
    
class CaracteristicaProducto(models.Model):
    id = models.AutoField(primary_key = True)
    caracteristica = models.CharField(max_length = 60, blank = False, null = True)
    valor = models.ManyToManyField(ValorCaracteristicaProducto, verbose_name="ValorCaracteristicaProducto")


    class Meta:
        verbose_name = 'CaracteristicaProducto'
        verbose_name_plural = 'CaracteristicasProductos'
        ordering = ['caracteristica']
    
    def __str__(self):
        return self.caracteristica
    
    
class Producto(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    descripcion = models.CharField(max_length = 120, blank = False, null = True)
    caracteristicaProducto = models.ForeignKey(CaracteristicaProducto, verbose_name="CaracteristicaProducto", on_delete=models.CASCADE)
    valorCaracteristicaProducto = models.ForeignKey(ValorCaracteristicaProducto, verbose_name="ValorCaracteristicaProducto", on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null = True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre + ' ' + self.caracteristicaProducto.caracteristica + ' ' + self.valorCaracteristicaProducto.valor
        
class Pedido(models.Model):
    id = models.AutoField(primary_key = True)
    paciente = models.ForeignKey(Paciente, verbose_name="Paciente", on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto, verbose_name="Producto")
    subtotal = models.DecimalField(max_digits=5, decimal_places=2)
    tipoDePago = models.ForeignKey(TipoDePago, verbose_name="TipoDePago", on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoPedido, verbose_name="EstadoPedido", on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']
    
    def __str__(self):
        return 'Pedido '+ self.paciente.nombre +' '+ self.paciente.apellido
    
    def getProductos(self):
        return self.producto.all()