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