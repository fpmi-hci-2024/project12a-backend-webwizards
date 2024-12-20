from django.urls import path
from . import views
from .views import OrderAPIView

urlpatterns = [
    path('orders/', OrderAPIView.as_view(), name='order_api'),
]