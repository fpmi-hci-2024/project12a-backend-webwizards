from django.urls import path
from . import views
from .views import OrderAPIView, OrderDetailView

urlpatterns = [
    path('', OrderAPIView.as_view(), name='order_api'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]