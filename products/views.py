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
