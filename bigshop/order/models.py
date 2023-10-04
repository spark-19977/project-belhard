import re

from django.contrib.auth import get_user_model
from django.db import models

from shop.models import Product


# Create your models here.
class UserData(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='registered_user_form')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    delivery = models.CharField(max_length=64, choices=[('delivery', 'delivery'), ('pickup', 'pickup')])
    address = models.CharField(max_length=250, null=True, blank=True, default='')
    postal_code = models.CharField(max_length=20, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.user.username}'


class UserOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='user_order')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    delivery = models.CharField(max_length=64, choices=[('delivery', 'delivery'), ('pickup', 'pickup')])
    address = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=60, choices=(
        ('in process', 'in process'),
        ('active', 'active'),
        ('processed', 'processed'),
        ('canceled', 'canceled'),
    ), default='in process')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]


    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(UserOrder,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
