from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import Cliente
from .serializers import ClienteSerializer
from .permissions import EsStaffOSoloLectura

class ClienteListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/clientes/ → lista paginada de clientes (usuario autenticado)
    POST /api/clientes/ → crea un cliente (solo staff)
    """

    queryset = Cliente.objects.prefetch_related('oportunidades').order_by('nombre')
    serializer_class = ClienteSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [EsStaffOSoloLectura]


class ClienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/clientes/<id>/   → detalle del cliente (usuario autenticado)
    PUT    /api/clientes/<id>/   → actualiza el cliente (solo staff)
    PATCH  /api/clientes/<id>/   → actualiza parcialmente (solo staff)
    DELETE /api/clientes/<id>/   → elimina el cliente (solo staff)
    """
    queryset = Cliente.objects.prefetch_related('oportunidades')
    serializer_class = ClienteSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [EsStaffOSoloLectura]
