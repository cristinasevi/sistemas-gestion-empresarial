from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_pedido', 'total', 'cliente')
    search_fields = ('cliente__nombre', 'cliente__email', 'id')
