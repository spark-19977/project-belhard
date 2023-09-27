from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView

from .forms import CartAddProductForm
from .cart import Cart
from shop.models import Product

# Create your views here.

class AddCart(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect('cart:cart_detail')

class DelCart(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')

class CartView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True})
        context['cart'] = cart
        return context

