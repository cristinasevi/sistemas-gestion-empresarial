from django.db import models
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

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.user} ({self.status})"
