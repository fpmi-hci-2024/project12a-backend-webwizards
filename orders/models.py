from django.db import models

from shop.models import Product, Profile
from addresses.models import Address
from users.models import Payment


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processed', 'Обработан'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, db_index=True)
    address = models.ForeignKey('addresses.Address', on_delete=models.CASCADE, verbose_name='Адрес', related_name='orders')
    payment = models.ForeignKey('users.Payment', on_delete=models.CASCADE, verbose_name='Платеж', related_name='orders')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)