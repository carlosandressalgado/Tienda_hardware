from django.test import TestCase, Client
from .models import Producto, Categoria, Carrito, ItemCarrito
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse

class CarritoTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear categoría obligatoria
        self.categoria = Categoria.objects.create(nombre="Accesorio")
        # Crear producto con todos los campos obligatorios
        self.producto = Producto.objects.create(
            codigo_producto="P001",
            nombre="Mouse Gamer",
            precio=15000,
            stock=10,
            categoria=self.categoria
        )

    def test_agregar_producto_crea_item(self):
        response = self.client.get(f'/agregar_al_carrito/{self.producto.id}/')
        carrito_id = self.client.session.get('carrito_id')
        carrito = Carrito.objects.get(id=carrito_id)
        item = ItemCarrito.objects.get(carrito=carrito, producto=self.producto)
        self.assertEqual(item.cantidad, 1)

    def test_incrementar_cantidad_existente(self):
        # Primer producto agregado
        self.client.get(f'/agregar_al_carrito/{self.producto.id}/')
        # Segundo agregado (mismo producto)
        self.client.get(f'/agregar_al_carrito/{self.producto.id}/')

        carrito_id = self.client.session.get('carrito_id')
        carrito = Carrito.objects.get(id=carrito_id)
        item = ItemCarrito.objects.get(carrito=carrito, producto=self.producto)
        self.assertEqual(item.cantidad, 2)

    def test_disminuir_cantidad_producto(self):
        # Agregamos 2 veces
        self.client.get(f'/agregar_al_carrito/{self.producto.id}/')
        self.client.get(f'/agregar_al_carrito/{self.producto.id}/')

        # Disminuimos cantidad
        self.client.get(f'/disminuir_cantidad/{self.producto.id}/')

        # Verificamos que la cantidad es 1
        carrito_id = self.client.session.get('carrito_id')
        carrito = Carrito.objects.get(id=carrito_id)
        item = ItemCarrito.objects.get(carrito=carrito, producto=self.producto)
        self.assertEqual(item.cantidad, 1)    

    def test_eliminar_producto_del_carrito(self):
        self.client.get(f'/agregar_al_carrito/{self.producto.id}/')

        carrito_id = self.client.session.get('carrito_id')
        carrito = Carrito.objects.get(id=carrito_id)
        item = ItemCarrito.objects.get(carrito=carrito, producto=self.producto)

        response = self.client.post(f'/eliminar/{item.id}/')

        items = ItemCarrito.objects.filter(carrito=carrito)
        self.assertEqual(items.count(), 0)

    def test_iniciar_pago_redirecciona(self):
        # Agregar producto para tener algo en el carrito
        self.client.get(f'/agregar_al_carrito/{self.producto.id}/')

        # Llamar a iniciar_pago
        response = self.client.get('/pagar/')

        # Verificar que hay redirección
        self.assertEqual(response.status_code, 302)
        self.assertIn('transbank', response.url)  # Verifica que sea una URL de Transbank

class RegistroUsuarioTests(TestCase):
    def setUp(self):
        self.client = Client()
    def test_registro_usuario_muestra_mensaje_y_redirige(self):
        datos = {
            'nombre': 'Juan Pérez',
            'usuario': 'juan123',
            'email': 'juan@example.com',
            'password': 'claveSegura2024',
        }
        response = self.client.post('/productos/registrar', datos, follow=True)
        self.assertTrue(User.objects.filter(username='juan123').exists())
        self.assertRedirects(response, '/productos', status_code=302, target_status_code=200)

        mensajes = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("usuario creado" in str(mensaje).lower() for mensaje in mensajes)
        )
        