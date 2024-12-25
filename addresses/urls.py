from django.urls import path
from .views import CityListAPIView, AddressByCityAPIView, AddressListAPIView

urlpatterns = [
    path('cities/', CityListAPIView.as_view(), name='city-list'),
    path('addresses/', AddressListAPIView.as_view(), name='address-list'),
    path('cities/<slug:slug>/addresses/', AddressByCityAPIView.as_view(), name='address-by-city'),
]