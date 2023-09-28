import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from shop.models import Product, Category
from order.models import UserOrder


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class OrderForm(serializers.ModelSerializer):
    product_ids = serializers.ListField(allow_empty=False)
    class Meta:
        media_type = 'asd'
        model = UserOrder
        exclude = ['user', 'status', 'paid']

    def validate(self, attrs):
        cd = super().validate(attrs)
        if cd['delivery'] == 'delivery':
            if not cd['address'] or not cd['postal_code']:
                raise ValidationError('if you choice delivery, you have enter address and postal code too')

        if not re.fullmatch(r'[+]?\d{10,12}', cd['phone']):
            raise ValidationError('please enter correct phone')

        for i in cd['product_ids']:
            if not isinstance(i, int):
                raise ValidationError('product ids must be int')

        return attrs

