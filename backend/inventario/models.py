from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Componente(models.Model): 
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo_interno = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Ej: RES-001")
    ubicacion = models.CharField(max_length=100, blank=True, null=True, help_text="Ej: Estante A, Gaveta 3")
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.codigo_interno:
            return f"[{self.codigo_interno}] {self.nombre} - Stock: {self.stock}"
        return f"{self.nombre} - Stock: {self.stock}"

class Pedido(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pedido: {self.componente.nombre} - Cantidad: {self.cantidad}"
    
class Devolucion(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    motivo = models.CharField(max_length=200, blank=True, null=True)
    fecha_devolucion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Devolución: {self.componente.nombre} - Motivo: {self.motivo}"

class HistorialMovimiento(models.Model):
    TIPO_CHOICES = [('SALIDA', 'Salida (Pedido)'), ('ENTRADA', 'Entrada (Devolución)')]
    
    componente_nombre = models.CharField(max_length=150)
    usuario_nombre = models.CharField(max_length=150)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo}: {self.componente_nombre} - {self.cantidad}"