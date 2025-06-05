from django.urls import path
from . import views

urlpatterns = [
    path('productos', views.productos, name="productos"),
    path('productos/login', views.login, name="login"),
    path('productos/registrar', views.registrar, name="registrar"),
    path('productos/categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('pagar/', views.iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),
    path('stock/', views.admin_stock, name='admin_stock'),
]
