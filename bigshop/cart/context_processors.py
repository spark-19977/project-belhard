from .cart import Cart


def cart_length(request):
    cart = Cart(request)
    return {'cart_length': cart.item_amount()}