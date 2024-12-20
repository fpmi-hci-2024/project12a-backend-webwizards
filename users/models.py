from django.contrib.auth.models import User
from django.db import models
from shop.models import Product

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_products = models.ManyToManyField('shop.Product', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.user.username
