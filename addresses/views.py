from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import City, Address
from .serializers import CitySerializer, AddressSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


# Create your views here.
@extend_schema_view(
    get=extend_schema(
        summary="Получение списка городов",
        description="Возвращает список всех доступных городов.",
        responses={
            200: CitySerializer(many=True),
            404: OpenApiResponse(
                response=None,
                description="Города не найдены."
            ),
        },
    ),
)
class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


@extend_schema_view(
    get=extend_schema(
        summary="Получение списка городов",
        description="Возвращает список всех доступных городов.",
        responses={
            200: CitySerializer(many=True),
            404: OpenApiResponse(
                response=None,
                description="Города не найдены."
            ),
        },
    ),
)
class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

@extend_schema_view(
    get=extend_schema(
        summary="Получение списка адресов",
        description="Возвращает список всех доступных адресов.",
        responses={
            200: AddressSerializer(many=True),
            404: OpenApiResponse(
                response=None,
                description="Адреса не найдены."
            ),
        },
    ),
)
class AddressListAPIView(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Получение адресов по городу",
        description="Возвращает список адресов, связанных с указанным городом.",
        responses={
            200: AddressSerializer(many=True),
            404: OpenApiResponse(
                response=None,
                description="Город не найден или адреса не найдены."
            ),
        },
    ),
)
class AddressByCityAPIView(ListAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        try:
            city = City.objects.get(slug=slug)
        except City.DoesNotExist:
            raise NotFound("Город не найден.")

        return Address.objects.filter(city=city)
