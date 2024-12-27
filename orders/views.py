from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, OrderCreateSerializer


# Create your views here.
@extend_schema_view(
    get=extend_schema(
        summary="Получение всех заказов пользователя",
        description="Получить список всех заказов, связанных с текущим пользователем. Если заказы отсутствуют, будет возвращен пустой список.",
        responses={
            200: OrderSerializer(many=True),
        },
    ),
    post=extend_schema(
        summary="Создание нового заказа на основе элементов корзины",
        description="Создать новый заказ для текущего пользователя, перенести все элементы из корзины в заказ. Если корзина пуста, будет возвращено сообщение об ошибке.",
        request=OrderCreateSerializer,  # Указываем, что запрос должен содержать OrderCreateSerializer
        responses={
            201: OrderSerializer,
            400: OpenApiResponse(
                response=None,
                description="Корзина пуста или отсутствуют адрес и платеж. Заказ не был создан."
            ),
        },
    ),
)
class OrderAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer  # Используем новый сериализатор

    def get(self, request):
        orders = Order.objects.filter(profile=request.user.profile)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = request.user.profile
        address_id = serializer.validated_data['address']
        payment_id = serializer.validated_data['payment']

        cart = Cart.objects.filter(profile=profile).first()
        if not cart or cart.total_items == 0:
            return Response({"detail": "Корзина пуста."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем новый заказ
        order = Order(profile=profile, address_id=address_id, payment_id=payment_id)
        order.save()

        # Переносим элементы из корзины в заказ
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )

        # Очищаем корзину
        cart.items.all().delete()

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        summary="Получение деталей заказа",
        description="Возвращает детали конкретного заказа и список его элементов. Доступно только для аутентифицированных пользователей.",
        responses={
            200: OpenApiResponse(
                response=None,
                description="Детали заказа и его элементы успешно возвращены."
            ),
            403: OpenApiResponse(
                response=None,
                description="Доступ запрещен. У вас нет прав на просмотр этого заказа."
            ),
            404: OpenApiResponse(
                response=None,
                description="Заказ не найден."
            ),
        },
    ),
)
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        if order.profile != request.user.profile:
            return Response({"detail": "У вас нет доступа к этому заказу."}, status=403)

        serializer = self.get_serializer(order)
        items = order.items.all()
        item_serializer = OrderItemSerializer(items, many=True)

        return Response({
            'order': serializer.data,
            'items': item_serializer.data
        })