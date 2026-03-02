from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    price = models.FloatField(_('price'))
    stock = models.IntegerField()
    on_sale = models.BooleanField(_('on sale'), default=False)

    def __str__(self):
        return self.name
