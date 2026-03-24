from django.db import models
from decimal import Decimal
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Model representing a product.
    Products can belong to multiple categories.
    """
    name = models.CharField(_('name'), max_length=100)
    price = models.FloatField(_('price'))
    stock = models.IntegerField()
    on_sale = models.BooleanField(_('on sale'), default=False)
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name=_('categories'),
        blank=True
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    # created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return f"{self.name} (${self.price})"


class Order(models.Model):
    """
    Model representing a customer order.
    Each order is associated with a user and contains multiple products.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        SHIPPED = 'shipped', _('Shipped')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('user')
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=21.00)
    total_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return f"Order #{self.id} - {self.get_status_display()}"
    
    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())
    
    def calcular_totales(self):
        """Calcula base, IVA y total sumando las líneas."""
        base = sum(item.total_price for item in self.items.all())
        self.total_base = Decimal(base)
        self.total_iva = self.total_base * (Decimal(str(self.iva_porcentaje)) / 100)
        self.total_pedido = self.total_base + self.total_iva
        self.save()
    
    def confirmar_pedido(self):
        """Lógica de transición de estado."""
        if self.items.count() == 0:
            raise ValueError("No se puede confirmar un pedido sin líneas.")
        if self.status != self.Status.PENDING:
            raise ValueError("Solo se pueden confirmar pedidos en estado pendiente.")
        
        self.status = self.Status.PROCESSING
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('order')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_('product')
    )
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        if not self.pk: # Only set price on creation
            self.price = self.product.price
        super().save(*args, **kwargs)

class Factura(models.Model):
    pedido = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='factura')
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_factura
