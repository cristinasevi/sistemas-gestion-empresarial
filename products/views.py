from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_add')

from django.views.generic import ListView
from django.contrib import messages
from .models import Order
import logging

logger = logging.getLogger(__name__)

class OrderListView(ListView):
    model = Order
    template_name = 'ventas/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

def get_queryset(self):
    try:
        queryset = super().get_queryset()
        
        # Filtro por búsqueda de cliente
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(user__username__icontains=search)
        
        return queryset.order_by('-created_at')
    except Exception:
        logger.error("Error al obtener los pedidos.", exc_info=True)
        messages.error(self.request, "No se encontraron pedidos.")
        return Order.objects.none()
