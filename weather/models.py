from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Имя пользователя')
    name = models.CharField(max_length=30, verbose_name='Имя города')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
