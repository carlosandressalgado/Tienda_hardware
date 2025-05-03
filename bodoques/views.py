from django.shortcuts import render,get_object_or_404, redirect
from .models import Categoria, Producto, Carrito, ItemCarrito
# Create your views here.
def productos(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def registrar(request):
    return render(request, 'registrar.html')

def productos_por_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'productos_por_categoria.html', {'categoria': categoria, 'productos': productos})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Obtén el carrito, si no existe, crea uno nuevo
    carrito_id = request.session.get('carrito_id')
    if not carrito_id:
        carrito = Carrito.objects.create()
        request.session['carrito_id'] = carrito.id
    else:
        carrito = get_object_or_404(Carrito, id=carrito_id)

    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
        item.save()

    return redirect('carrito')

def carrito(request):
    carrito_id = request.session.get('carrito_id')
    if not carrito_id:
        carrito = None
        total = 0
    else:
        carrito = get_object_or_404(Carrito, id=carrito_id)
        total = sum(item.producto.precio * item.cantidad for item in carrito.items.all())
    
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

def eliminar_del_carrito(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(ItemCarrito, id=item_id)
        item.delete()
    return redirect('/carrito/')