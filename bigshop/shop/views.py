from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, DetailView


from . import models
from .forms import UserRegistrationForm
from .tokens import account_activation_token
from .models import Product, Category
from . import tasks
from cart.forms import CartAddProductForm


# Create your views here.


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request,
                      'registration/register_done.html',)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.is_active = False
            # Save the User object
            new_user.save()
            current_site = get_current_site(request)
            to_email = user_form.cleaned_data.get('email')

            tasks.send_email_confirm.delay(current_site_domain=current_site.domain,
                                           new_user_pk=new_user.pk,
                                           to_email=to_email)
            return render(request,
                          'registration/register_sended_email.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})
class ProductListView(ListView):
    paginate_by = 12
    model = models.Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_product_form = CartAddProductForm()
        context['add_product_form'] = add_product_form
        return context

class CategoryDetailView(ListView):
    # model = models.Category
    template_name = 'shop/categoty_product_list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        queryset = Product.objects.filter(category=category).order_by(['pk'])
        return queryset