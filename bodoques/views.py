from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Categoria, Producto, Carrito, ItemCarrito

# Webpay Plus
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions

# Configuración única de Webpay para el entorno de prueba
options = WebpayOptions(
    commerce_code='597055555532',
    api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
    integration_type=IntegrationType.TEST
)

transaction = Transaction(options)

def productos(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def registrar(request):
    return render(request, 'registrar.html')

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'productos_por_categoria.html', {'categoria': categoria, 'productos': productos})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

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
    return redirect('carrito')

def iniciar_pago(request):
    carrito_id = request.session.get('carrito_id')
    if not carrito_id:
        return redirect('carrito')

    carrito = get_object_or_404(Carrito, id=carrito_id)
    total = sum(item.producto.precio * item.cantidad for item in carrito.items.all())

    buy_order = f"orden_{carrito.id}_{int(timezone.now().timestamp())}"
    session_id = str(request.session.session_key)
    amount = total
    return_url = request.build_absolute_uri('/confirmar_pago/')

    try:
        response = transaction.create(buy_order, session_id, amount, return_url)
        return redirect(f"{response['url']}?token_ws={response['token']}")
    except Exception as e:
        return HttpResponse(f"Error al iniciar el pago: {e}")

def confirmar_pago(request):
    token = request.GET.get('token_ws')
    if not token:
        return HttpResponse("No se recibió token de pago.")

    try:
        response = transaction.commit(token)

        if response['status'] == 'AUTHORIZED':
            request.session.pop('carrito_id', None)
            return render(request, 'pago_exitoso.html', {'response': response})
        else:
            return render(request, 'pago_fallido.html', {'response': response})
    except Exception as e:
        return HttpResponse(f"Error al confirmar el pago: {e}")
