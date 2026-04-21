from django.urls import path
from . import views
from .api_views import ClienteListCreateAPIView, ClienteRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', views.crm_dashboard, name='crm_dashboard'),
    # API endpoints
    path('api/clientes/', ClienteListCreateAPIView.as_view(), name='api_cliente_list'),
    path('api/clientes/<int:pk>/', ClienteRetrieveUpdateDestroyAPIView.as_view(), name='api_cliente_detail'),
]
