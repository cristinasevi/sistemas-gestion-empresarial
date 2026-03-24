from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Factura

@receiver(post_save, sender=Order)
def generar_factura_automatica(sender, instance, **kwargs):
    if instance.status == Order.Status.PROCESSING:
        if not Factura.objects.filter(pedido=instance).exists():
            num = f"FAC-{instance.id:06d}"
            Factura.objects.create(pedido=instance, numero_factura=num)
