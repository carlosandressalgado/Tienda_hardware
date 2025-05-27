from django.urls import path
from .views import productos, login, registrar, productos_por_categoria, agregar_al_carrito, carrito, eliminar_del_carrito, iniciar_pago, confirmar_pago

urlpatterns = [
    path('productos', productos, name="productos"),
    path('productos/login', login, name="login"),
    path('productos/registrar', registrar, name="registrar"),
    path('productos/categoria/<int:categoria_id>/', productos_por_categoria, name='productos_por_categoria'),
    path('carrito/', carrito, name='carrito'),
    path('agregar_al_carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),

    path('pagar/', iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),

]