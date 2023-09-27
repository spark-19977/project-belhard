from django.urls import path
from .views import AddCart, CartView, DelCart

app_name = 'cart'
urlpatterns = [
    path('add/<product_id>', AddCart.as_view(), name='add_cart'),
    path('delete/<product_id>', DelCart.as_view(), name='del_cart'),
    path('', CartView.as_view(), name='cart_detail'),
]