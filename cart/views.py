from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, extend_schema_view, OpenApiParameter
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
@extend_schema_view(
    get=extend_schema(
        summary="Получение корзины",
        description="Получить детали текущей корзины пользователя.",
        responses={
            200: CartSerializer,
            404: OpenApiResponse(
                response=None,
                description="Корзина не найдена."
            ),
        },
    ),
    post=extend_schema(
        summary="Добавление товара в корзину",
        description="Добавить новый товар в корзину пользователя.",
        request=CartItemSerializer,
        responses={
            201: CartItemSerializer,
            400: OpenApiResponse(
                response=None,
                description="Ошибка валидации данных."
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                summary="Добавление товара в корзину",
                value={
                    "product": 1,  # ID продукта
                    "quantity": 2,  # Количество
                },
            ),
        ],
    ),
    delete=extend_schema(
        summary="Очистка корзины",
        description="Удалить все товары из корзины текущего пользователя.",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Корзина успешно очищена."
            ),
        },
    ),
)
class CartAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_cart(self):
        return Cart.objects.get(profile=self.request.user.profile)

    def get(self, request, *args, **kwargs):
        cart = self.get_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        item_serializer = CartItemSerializer(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save(cart=cart)
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        cart = self.get_cart()
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator(csrf_exempt, name='dispatch')
@extend_schema_view(
    delete=extend_schema(
        summary="Удаление товара из корзины",
        description="Удалить товар из корзины текущего пользователя по ID элемента.",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Элемент успешно удален."
            ),
            404: OpenApiResponse(
                response=None,
                description="Элемент не найден."
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                summary="Удаление товара с ID 1 из корзины",
                value={
                    "id": 1,
                },
            ),
        ],
    ),
)
class CartItemAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_cart(self):
        return Cart.objects.get(profile=self.request.user.profile)

    def get_cart_item(self, pk):
        cart = self.get_cart()
        return cart.items.get(id=pk)

    def delete(self, request, *args, **kwargs):
        try:
            cart_item = self.get_cart_item(kwargs['pk'])
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Элемент не найден."}, status=status.HTTP_404_NOT_FOUND)

