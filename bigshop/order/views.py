from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView, ListView

from cart.cart import Cart

from .forms import OrderForm
from .models import UserData, OrderItem, UserOrder


class MyOrders(ListView):
    template_name = 'order/order_list.html'
    paginate_by = 10
    context_object_name = 'orders'

    def get_queryset(self):
        return UserOrder.objects.filter(user=self.request.user).order_by('-updated')

# Create your views here.
class ProfileInfo(UpdateView):
    fields = '__all__'

    def get_success_url(self):
        return reverse('shop:index')

    def get_object(self, queryset=None):
        try:
            user_data = self.request.user.registered_user_form
        except Exception as err:
            user_data = UserData()
        return user_data
    def get_form_class(self):
        return OrderForm




class EnterOrderData(View):
    def get(self, request):
        form = OrderForm()
        if request.user.is_authenticated:
            try:
                userdata = request.user.registered_user_form.__dict__
                userdata.pop('id')
                userdata.pop('user_id')
                userdata.pop('_state')
                form = OrderForm(userdata)
            except Exception as err:
                print(err)
        cart = Cart(request)
        return render(request, 'order/create_order.html', dict(cart=cart, form=form))

    def post(self, request):
        form = OrderForm(request.POST)
        cart = Cart(request)
        if not cart:
            return HttpResponse(status=404, content='you dont have items in your cart')
        if form.is_valid():
            if request.user.is_authenticated:
                form.save(commit=False)
                try:
                    user_data = request.user.registered_user_form
                    user_data.delete()
                except: ...

                user_data = UserData(**form.cleaned_data)
                user_data.user = request.user
                user_data.save()

                order = form.save(commit=False)
                order.user = request.user
                order.save()
            else:
                order = form.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'order/created.html')
        return render(request, 'order/create_order.html', dict(cart=cart, form=form))
    # template_name = 'order/create_order.html'
    #
    # def get_context_data(self, **kwargs):
    #     cart = Cart(self.request)
    #     form = OrderForm()
    #     if self.request.user.is_authenticated:
    #         try:
    #             form = OrderForm(self.request.user.registered_user_form)
    #         except Exception as err:
    #             print(err)
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = form
    #     context['cart'] = cart
    #     return context


# def create_order(request: HttpRequest):
#     form = OrderForm(request.POST)
#     cart = Cart(request)
#     if request.user.is_authenticated:
#         try:
#             userdata = request.user.registered_user_form.__dict__
#             userdata.pop('id')
#             userdata.pop('user_id')
#             userdata.pop('_state')
#             form = OrderForm(userdata)
#         except Exception as err:
#             data = UserData()
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if not cart:
#             return HttpResponse(status=404, content='you dont have items in your cart')
#         if form.is_valid():
#             cd = form.cleaned_data
#             if request.user.is_authenticated:
#                 form.save(commit=False)
#                 user_data = request.user.registered_user_form
#                 user_data.user = request.user
#                 user_data.save()
#             order = form.save()
#
#             for item in cart:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=item['product'],
#                     price=item['price'],
#                     quantity=item['quantity']
#                 )
#             cart.clear()
#             return render(request, 'order/created.html')
#     return render(request, 'order/create_order.html', dict(cart=cart, form=form))


