from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    total_oportunidades = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre',
            'email',
            'telefono',
            'empresa',
            'fecha_registro',
            'total_oportunidades',
        ]
        read_only_fields = ['id', 'fecha_registro']
    
    def get_total_oportunidades(self, obj):
        return obj.oportunidades.count()
