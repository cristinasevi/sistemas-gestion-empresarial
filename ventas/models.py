from django.db import models
from core.models import Cliente

class Pedido(models.Model):
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name='pedidos')

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nombre} - Total: {self.total}"
