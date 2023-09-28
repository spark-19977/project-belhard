from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey('category', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    descr = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    amount = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='product/', default='no_image.jpg')
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    product = models.ForeignKey('product', models.DO_NOTHING)
    amount = models.SmallIntegerField()
