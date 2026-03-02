from django.urls import path
from .views import ProductCreateView, OrderListView

urlpatterns = [
    path('add/', ProductCreateView.as_view(), name='product_add'),
    path('orders/', OrderListView.as_view(), name='order-list'),
]
