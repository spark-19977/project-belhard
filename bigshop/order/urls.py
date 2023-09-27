from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.EnterOrderData.as_view(), name='order_create'),
    path('profile_info/', views.ProfileInfo.as_view(), name='profile_info'),
    path('my_orders/', views.MyOrders.as_view(), name='my_orders'),
]