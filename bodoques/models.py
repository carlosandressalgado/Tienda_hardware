from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    codigo_producto = models.CharField(max_length=200, unique=True)    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
class Carrito(models.Model):
    # En vez de tener una relación con User, usaremos una clave primaria
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Carrito {self.id}"

class ItemCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"
