from rest_framework import serializers

from addresses.models import Address
from addresses.serializers import AddressSerializer
from users.models import Payment
from users.serializers import PaymentSerializer
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    address = AddressSerializer()
    payment = PaymentSerializer()

    class Meta:
        model = Order
        fields = ['id', 'created', 'updated', 'status', 'items', 'address', 'payment']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class OrderCreateSerializer(serializers.ModelSerializer):
    address = serializers.IntegerField()  # Ожидаем идентификатор адреса
    payment = serializers.IntegerField()  # Ожидаем идентификатор платежа

    class Meta:
        model = Order
        fields = ['address', 'payment']  # Указываем только необходимые поля

    def validate(self, attrs):
        # Проверяем наличие адреса и платежа в базе данных
        if not Address.objects.filter(id=attrs['address']).exists():
            raise serializers.ValidationError("Адрес не найден.")
        if not Payment.objects.filter(id=attrs['payment']).exists():
            raise serializers.ValidationError("Платеж не найден.")
        return attrs