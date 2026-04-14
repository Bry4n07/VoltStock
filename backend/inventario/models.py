from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Componente(models.Model): 
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"

class Pedido(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pedido: {self.componente.nombre} - Cantidad: {self.cantidad}"
    
class Devolucion(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=200)
    fecha_devolucion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Devolución: {self.componente.nombre} - Motivo: {self.motivo}"