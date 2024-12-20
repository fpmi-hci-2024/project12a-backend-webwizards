from django.urls import path
from . import views
from .views import CartAPIView, CartItemAPIView

urlpatterns = [
    path('', CartAPIView.as_view(), name='cart'),
    path('items/<int:pk>/', CartItemAPIView.as_view(), name='cart-item'),
]