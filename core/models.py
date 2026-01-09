from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    dni = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"
