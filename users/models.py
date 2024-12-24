from django.db import models
from django.contrib.auth.models import User
from shop.models import Profile

class Payment(models.Model):
    profile = models.ForeignKey('shop.Profile', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.payment_type} - {self.card_number[-4:]}"