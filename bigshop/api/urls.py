from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import Order, ProductDetail, ProductList, CategoryList

# router = DefaultRouter()
# router.register('products', ProductViewSet)
# router.register('order', Order)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('order/', Order.as_view(), name='order'),
    # path('', include(router.urls)),
    path('categories/', CategoryList.as_view()),
    path('products/', ProductList.as_view()),
    path('products/<int:pk>', ProductDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]