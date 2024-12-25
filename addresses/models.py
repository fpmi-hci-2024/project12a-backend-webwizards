from django.db import models
from django.utils.text import slugify


# Create your models here.

class City(models.Model):
    REGION_CHOICES = [
        ('minsk', 'Минская область'),
        ('grodno', 'Гродненская область'),
        ('vitebsk', 'Витебская область'),
        ('gomel', 'Гомельская область'),
        ('mogilev', 'Могилевская область'),
        ('brest', 'Брестская область'),
    ]

    name = models.CharField(max_length=255)
    region = models.CharField(max_length=50, choices=REGION_CHOICES, verbose_name='Область')
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    name = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return f"{self.city} - {self.name}"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
