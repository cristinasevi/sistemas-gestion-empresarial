from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Product, Category, Order, OrderItem, Factura

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('order_link', 'product', 'quantity', 'price', 'total_price_display')
    fields = ('order_link', 'product', 'quantity', 'price', 'total_price_display')

    def order_link(self, obj):
        url = reverse('admin:products_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.order))
    order_link.short_description = _('order')
    order_link.admin_order_field = 'order'

    def total_price_display(self, obj):
        return f"${obj.total_price}"
    total_price_display.short_description = _('total price')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'pedido', 'fecha_emision')
    search_fields = ('numero_factura', 'pedido__id')
    readonly_fields = ('numero_factura', 'pedido', 'fecha_emision')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.
    """
    list_display = ('name', 'product_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Number of Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for the Product model with category support.
    """
    list_display = ('name', 'price', 'on_sale', 'display_categories', 'created_at')
    list_filter = ('on_sale', 'categories', 'created_at')
    search_fields = ('name',)
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('name', 'stock', 'price', 'on_sale')
        }),
        ('Categories', {
            'fields': ('categories',)
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'
