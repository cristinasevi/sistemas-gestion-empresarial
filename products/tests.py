from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Order, OrderItem, Product

User = get_user_model()

class PedidoLogicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.product = Product.objects.create(name='Producto Test', price=100, stock=10)
    
    def test_calculo_total_iva(self):
        order = Order.objects.create(user=self.user, iva_porcentaje=21)
        OrderItem.objects.create(order=order, product=self.product,quantity=1, price=100)
        
        order.calcular_totales()
        
        self.assertEqual(order.total_base, Decimal('100.00'))
        self.assertEqual(order.total_iva, Decimal('21.00'))
        self.assertEqual(order.total_pedido, Decimal('121.00'))

    def test_confirmar_pedido(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=100)

        order.confirmar_pedido()

        self.assertEqual(order.status, Order.Status.PROCESSING)

    def test_confirmar_pedido_sin_lineas(self):
        order = Order.objects.create(user=self.user)

        with self.assertRaises(ValueError):
            order.confirmar_pedido()
    
    def test_confirmar_pedido_ya_confirmado(self):
        order = Order.objects.create(user=self.user, status=Order.Status.PROCESSING)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=100)

        with self.assertRaises(ValueError):
            order.confirmar_pedido()
