from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, re_path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('', include('django.contrib.auth.urls')),
    path('activate/<uidb64>/<token>/',
         views.activate, name='activate'),
    path('register/', views.register, name='register'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),


]
