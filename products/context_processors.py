from django.conf import settings

def fiscal(request):
    return {
        'MONEDA': settings.MONEDA,
        'IVA': settings.IVA,
    }
