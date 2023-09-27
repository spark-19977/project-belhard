from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ProductSerializer, Product, OrderForm
from rest_framework.filters import BaseFilterBackend

from order.models import UserData, OrderItem, UserOrder


class ProductViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


class Order(APIView):
    serializer_class = OrderForm

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OrderForm(data=request.data)
        if serializer.is_valid():
            try:
                user_data = request.user.registered_user_form
                user_data.delete()
            except:
                ...
            cd = dict(**serializer.validated_data)
            cd.pop('product_ids')
            user_data = UserData(**cd)
            user_data.user = request.user
            user_data.save()
            # print(cd)
            order = UserOrder(**cd)
            order.user = request.user
            order.save()
            # order = serializer.save(user=request.user)
            # order.user = request.user
            # order.save()

            for product_id in serializer.validated_data['product_ids']:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=1
                )

            return Response({'order_id':order.id}, status=201)

        return Response(serializer.errors, status=400)
