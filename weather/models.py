from django.db import models
from django.contrib.auth.models import User
from .choices import TEMPERATURE_CHOICES

class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Имя пользователя')
    name = models.CharField(max_length=30, verbose_name='Имя города')
    temperature_unit = models.CharField(max_length=1, choices=TEMPERATURE_CHOICES, default='C', verbose_name='Единица измерения')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
