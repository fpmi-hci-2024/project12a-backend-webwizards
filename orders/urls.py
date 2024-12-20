from django.urls import path
from . import views
from .views import OrderAPIView

urlpatterns = [
    path('', OrderAPIView.as_view(), name='order_api'),
]